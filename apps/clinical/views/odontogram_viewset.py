from apps.clinical.filters import OdontogramFilter
from apps.clinical.models import Odontogram
from apps.clinical.serializers import OdontogramSerializer
from apps.common.viewsets import BaseTenantViewSet


class OdontogramViewSet(BaseTenantViewSet):
    queryset = Odontogram.objects.select_related("appointment")
    serializer_class = OdontogramSerializer
    required_tenant_permission = "edit_clinical_chart"

    filterset_class = OdontogramFilter
    search_fields = []
    ordering_fields = ["id", "created_at", "appointment"]
