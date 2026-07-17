import django_filters

from apps.appointments.models import ClinicAsset
from apps.appointments.serializers import ClinicAssetSerializer
from apps.common.viewsets import BaseTenantViewSet


class ClinicAssetFilter(django_filters.FilterSet):
    class Meta:
        model = ClinicAsset
        fields = ["asset_type", "is_operational"]


class ClinicAssetViewSet(BaseTenantViewSet):
    queryset = ClinicAsset.objects.all()
    serializer_class = ClinicAssetSerializer
    required_tenant_permission = "manage_appointments"

    filterset_class = ClinicAssetFilter
    search_fields = ["name"]
    ordering_fields = ["id", "name", "asset_type"]
