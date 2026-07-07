from apps.common.viewsets import BasePlatformViewSet
from apps.platform.serializers import TenantSerializer
from apps.tenants.filters import TenantFilter
from apps.tenants.models import Tenant


class TenantViewSet(BasePlatformViewSet):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
    required_module_codename = "manage_tenants"

    filterset_class = TenantFilter
    search_fields = ["name", "slug"]
    ordering_fields = ["id", "name", "created_at", "updated_at"]
