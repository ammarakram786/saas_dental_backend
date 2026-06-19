"""Tenant lifecycle services."""
from __future__ import annotations

from django.db import transaction

from apps.tenants.models import Tenant, TenantPermission, TenantRole

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
