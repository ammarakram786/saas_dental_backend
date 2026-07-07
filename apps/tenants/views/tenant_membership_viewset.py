from apps.common.viewsets import BaseTenantViewSet
from apps.tenants.filters import TenantMembershipFilter
from apps.tenants.models import TenantMembership
from apps.tenants.serializers import TenantMembershipSerializer


class TenantMembershipViewSet(BaseTenantViewSet):
    queryset = TenantMembership.objects.select_related("user", "role", "tenant")
    serializer_class = TenantMembershipSerializer
    required_tenant_permission = "manage_members"

    filterset_class = TenantMembershipFilter
    search_fields = [
        "user__username",
        "user__email",
        "user__first_name",
        "user__last_name",
    ]
    ordering_fields = ["id", "created_at", "is_active"]
