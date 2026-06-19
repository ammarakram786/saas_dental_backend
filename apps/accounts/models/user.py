from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_super_admin = models.BooleanField(
        default=False,
        help_text="Platform super administrator; bypasses all RBAC constraints.",
    )
    platform_role = models.ForeignKey(
        "platform.PlatformRole",
        null=True,
        blank=True,
        default=None,
        on_delete=models.SET_NULL,
        related_name="users",
        help_text="Control-plane role. Standard tenant users leave this empty.",
    )
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    # -- Platform (control plane) -------------------------------------------------
    def has_platform_module(self, codename: str) -> bool:
        """Whether this user may access the given platform module codename."""
        if self.is_super_admin:
            return True
        role = self.platform_role
        if role is None or not role.is_active:
            return False

        from apps.common.cache import get_platform_role_modules

        return codename in get_platform_role_modules(role)

    # -- Tenant (data plane) ------------------------------------------------------
    def _active_membership(self, tenant):
        from apps.tenants.models import TenantMembership

        return (
            TenantMembership.objects.filter(
                user=self, tenant=tenant, is_active=True
            )
            .select_related("role")
            .first()
        )

    def is_tenant_member(self, tenant) -> bool:
        if self.is_super_admin:
            return True
        return self._active_membership(tenant) is not None

    def tenant_role(self, tenant):
        """Return the user's active :class:`TenantRole` in ``tenant`` or ``None``."""
        membership = self._active_membership(tenant)
        return membership.role if membership else None

    def has_tenant_permission(self, tenant, codename: str) -> bool:
        if self.is_super_admin:
            return True
        role = self.tenant_role(tenant)
        if role is None or not role.is_active:
            return False

        from apps.common.cache import get_tenant_role_permissions

        return codename in get_tenant_role_permissions(role)
