"""Layered RBAC permission classes.

Two planes are enforced here:
- Platform (control plane) via :class:`HasPlatformModuleAccess`.
- Tenant (data plane) via :class:`IsTenantMember` / :class:`HasTenantPermission`.

A platform super admin bypasses every check via :class:`AuthContext`.
"""
from __future__ import annotations

from rest_framework.permissions import BasePermission


def _auth_context(request):
    user = getattr(request, "user", None)
    if user is None or not user.is_authenticated:
        return None

    ctx = getattr(request, "auth_context", None)
    if ctx is None:
        from apps.accounts.services import resolve_auth_context

        ctx = resolve_auth_context(user, getattr(request, "tenant", None))
        request.auth_context = ctx
    return ctx


class HasPlatformModuleAccess(BasePermission):
    """Grants access when the user's platform role includes ``required_module_codename``."""

    message = "You do not have access to this platform module."

    def has_permission(self, request, view) -> bool:
        ctx = _auth_context(request)
        if ctx is None:
            return False

        codename = getattr(view, "required_module_codename", None)
        if not codename:
            return False
        return ctx.has_platform_module(codename)


class IsTenantMember(BasePermission):
    """Requires a resolved ``request.tenant`` and an active membership in it."""

    message = "You are not a member of this tenant."

    def has_permission(self, request, view) -> bool:
        ctx = _auth_context(request)
        if ctx is None:
            return False

        tenant = getattr(request, "tenant", None)
        if tenant is None:
            return False
        return ctx.is_tenant_member()


class HasTenantPermission(BasePermission):
    """Checks ``view.required_tenant_permission`` against the membership's role.

    Falls back to plain membership when no specific permission is declared.
    """

    message = "Your tenant role does not grant this permission."

    def has_permission(self, request, view) -> bool:
        ctx = _auth_context(request)
        if ctx is None:
            return False

        tenant = getattr(request, "tenant", None)
        if tenant is None:
            return False

        codename = getattr(view, "required_tenant_permission", None)
        if not codename:
            return ctx.is_tenant_member()
        return ctx.has_tenant_permission(codename)
