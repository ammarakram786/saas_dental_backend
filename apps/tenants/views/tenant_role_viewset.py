from apps.common.viewsets import BaseTenantViewSet
from apps.tenants.filters import TenantRoleFilter
from apps.tenants.models import TenantRole
from apps.tenants.serializers import TenantRoleSerializer


class TenantRoleViewSet(BaseTenantViewSet):
    queryset = TenantRole.objects.prefetch_related("permissions")
    serializer_class = TenantRoleSerializer
    required_tenant_permission = "manage_members"

    filterset_class = TenantRoleFilter
    search_fields = ["name", "slug", "description"]
    ordering_fields = ["id", "name", "slug", "created_at"]
