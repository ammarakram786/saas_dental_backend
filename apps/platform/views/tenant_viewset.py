from apps.platform.models import PlatformAuditEvent
from apps.platform.serializers import TenantSerializer
from apps.tenants.filters import TenantFilter
from apps.tenants.models import Tenant
from apps.common.viewsets import BasePlatformViewSet


class TenantViewSet(BasePlatformViewSet):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
    required_module_codename = "manage_tenants"

    filterset_class = TenantFilter
    search_fields = ["name", "slug"]
    ordering_fields = ["id", "name", "created_at", "updated_at"]

    def perform_update(self, serializer):
        previous = self.get_object()
        was_active = previous.is_active
        tenant = serializer.save()
        if was_active and not tenant.is_active:
            PlatformAuditEvent.objects.create(
                actor=getattr(self.request.user, "username", "system"),
                action="suspended tenant",
                target=tenant.slug,
                severity="warning",
                category="security",
            )
        elif not was_active and tenant.is_active:
            PlatformAuditEvent.objects.create(
                actor=getattr(self.request.user, "username", "system"),
                action="activated tenant",
                target=tenant.slug,
                severity="info",
                category="security",
            )
