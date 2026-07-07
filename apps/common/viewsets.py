"""DRY base viewsets enforcing tenant isolation and platform gating."""
from __future__ import annotations

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated

from apps.common.permissions import (
    HasPlatformModuleAccess,
    HasTenantPermission,
    IsTenantMember,
)


class BaseTenantViewSet(viewsets.ModelViewSet):
    """Base for tenant-scoped (data-plane) endpoints.

    ``get_queryset`` always filters by ``request.tenant`` so a developer cannot
    accidentally leak rows across tenants, and ``perform_create`` stamps the
    active tenant onto new objects.

    Set ``required_tenant_permission`` on the subclass to gate by a dynamic
    role permission codename; otherwise active membership is sufficient.
    """

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    permission_classes = [IsAuthenticated, IsTenantMember, HasTenantPermission]
    required_tenant_permission: str | None = None

    @property
    def tenant(self):
        return getattr(self.request, "tenant", None)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.tenant is None:
            return queryset.none()
        return queryset.filter(tenant=self.tenant)

    def perform_create(self, serializer):
        serializer.save(tenant=self.tenant)


class BasePlatformViewSet(viewsets.ModelViewSet):
    """Base for platform-management (control-plane) endpoints.

    Subclasses must declare ``required_module_codename`` to gate access against
    the user's platform role.
    """

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    permission_classes = [IsAuthenticated, HasPlatformModuleAccess]
    required_module_codename: str | None = None
