from apps.clinical.filters.prescription import PrescriptionFilter
from apps.clinical.models import Prescription
from apps.clinical.serializers import PrescriptionSerializer
from apps.common.viewsets import BaseTenantViewSet


class PrescriptionViewSet(BaseTenantViewSet):
    queryset = Prescription.objects.select_related("clinical_note")
    serializer_class = PrescriptionSerializer
    required_tenant_permission = "edit_clinical_chart"

    filterset_class = PrescriptionFilter
    search_fields = []
    ordering_fields = ["id", "created_at"]
