from __future__ import annotations

from dataclasses import dataclass

from apps.accounts.models import PatientUserProfile, PlatformUserProfile, User
from apps.tenants.models import Tenant, TenantMembership


@dataclass
class AuthContext:
    user: User
    platform: PlatformUserProfile | None
    tenant_membership: TenantMembership | None
    patient: PatientUserProfile | None

    def is_platform_super_admin(self) -> bool:
        return bool(self.platform and self.platform.is_super_admin)

    def has_platform_module(self, codename: str) -> bool:
        if self.is_platform_super_admin():
            return True
        if self.platform is None:
            return False
        return self.platform.has_module(codename)

    def is_tenant_member(self) -> bool:
        if self.is_platform_super_admin():
            return True
        return self.tenant_membership is not None

    def has_tenant_permission(self, codename: str) -> bool:
        if self.is_platform_super_admin():
            return True
        if self.tenant_membership is None:
            return False
        role = self.tenant_membership.role
        if not role.is_active:
            return False

        from apps.common.cache import get_tenant_role_permissions

        return codename in get_tenant_role_permissions(role)

    def is_patient(self) -> bool:
        return self.patient is not None


def resolve_auth_context(user: User, tenant: Tenant | None = None) -> AuthContext:
    platform = (
        PlatformUserProfile.objects.select_related("role")
        .filter(user=user)
        .first()
    )
    patient = PatientUserProfile.objects.filter(user=user).first()

    membership = None
    if tenant is not None:
        membership = (
            TenantMembership.objects.filter(
                user=user, tenant=tenant, is_active=True
            )
            .select_related("role")
            .first()
        )

    return AuthContext(
        user=user,
        platform=platform,
        tenant_membership=membership,
        patient=patient,
    )
