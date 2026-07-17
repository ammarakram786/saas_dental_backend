"""Tenant lifecycle services."""
from __future__ import annotations

from dataclasses import dataclass

from django.contrib.auth import get_user_model
from django.db import transaction

from apps.tenants.models import Tenant, TenantMembership, TenantPermission, TenantRole

User = get_user_model()


class TenantProvisioningError(Exception):
    def __init__(self, detail: dict):
        self.detail = detail
        super().__init__(detail)

# Default role -> permission-codename mapping. ``None`` means "all permissions".
DEFAULT_ROLE_DEFINITIONS: dict[str, dict] = {
    "admin": {
        "name": "Administrator",
        "description": "Full control over the tenant.",
        "permissions": None,
    },
    "manager": {
        "name": "Manager",
        "description": "Manage day-to-day operations.",
        "permissions": {
            "manage_members",
            "manage_appointments",
            "view_reports",
            "edit_clinical_chart",
            "manage_treatment_plans",
            "manage_billing",
        },
    },
    "member": {
        "name": "Member",
        "description": "Standard tenant member with basic access.",
        "permissions": {
            "view_appointments",
        },
    },
}


@transaction.atomic
def seed_default_roles(tenant: Tenant) -> list[TenantRole]:
    """Create the baseline system roles for ``tenant``.

    Idempotent: existing roles (matched by slug) are reused and their permission
    sets reconciled, so this can run safely on every tenant creation.
    """
    all_permissions = list(TenantPermission.objects.filter(is_active=True))
    by_codename = {perm.codename: perm for perm in all_permissions}

    created_roles: list[TenantRole] = []
    for slug, definition in DEFAULT_ROLE_DEFINITIONS.items():
        role, _ = TenantRole.objects.get_or_create(
            tenant=tenant,
            slug=slug,
            defaults={
                "name": definition["name"],
                "description": definition["description"],
                "is_system": True,
                "is_active": True,
            },
        )

        wanted = definition["permissions"]
        if wanted is None:
            role.permissions.set(all_permissions)
        else:
            role.permissions.set(
                [by_codename[c] for c in wanted if c in by_codename]
            )
        created_roles.append(role)

    return created_roles


@dataclass(frozen=True)
class TenantProvisioningResult:
    tenant: Tenant
    admin_user: User
    membership: TenantMembership
    created_user: bool


def _username_from_email(email: str) -> str:
    base = (email.split("@", 1)[0] or "user")[:150]
    candidate = base
    suffix = 1
    while User.objects.filter(username=candidate).exists():
        candidate = f"{base}{suffix}"[:150]
        suffix += 1
    return candidate


@transaction.atomic
def provision_tenant_with_admin(
    *,
    name: str,
    slug: str,
    is_active: bool = True,
    admin_email: str,
    admin_first_name: str = "",
    admin_last_name: str = "",
    admin_password: str | None = None,
) -> TenantProvisioningResult:
    """Create a tenant and assign an administrator membership in one transaction."""
    tenant = Tenant.objects.create(name=name, slug=slug, is_active=is_active)
    admin_role = TenantRole.objects.get(tenant=tenant, slug="admin")

    normalized_email = admin_email.strip().lower()
    user = User.objects.filter(email__iexact=normalized_email).first()
    created_user = False

    if user is None:
        if not admin_password:
            raise TenantProvisioningError(
                {"admin_user": {"password": ["Password is required for a new user."]}}
            )
        user = User.objects.create_user(
            username=_username_from_email(normalized_email),
            email=normalized_email,
            password=admin_password,
            first_name=admin_first_name.strip(),
            last_name=admin_last_name.strip(),
        )
        created_user = True
    elif TenantMembership.objects.filter(user=user, tenant=tenant).exists():
        raise TenantProvisioningError(
            {"admin_user": {"email": ["User is already a member of this tenant."]}}
        )

    membership = TenantMembership.objects.create(
        user=user,
        tenant=tenant,
        role=admin_role,
        is_active=True,
    )

    return TenantProvisioningResult(
        tenant=tenant,
        admin_user=user,
        membership=membership,
        created_user=created_user,
    )
