from apps.clinical.filters import TreatmentPlanFilter
from apps.clinical.models import TreatmentPlan
from apps.clinical.serializers import TreatmentPlanSerializer
from apps.common.viewsets import BaseTenantViewSet


class TreatmentPlanViewSet(BaseTenantViewSet):
    queryset = TreatmentPlan.objects.select_related("appointment")
    serializer_class = TreatmentPlanSerializer
    required_tenant_permission = "manage_treatment_plans"

    filterset_class = TreatmentPlanFilter
    search_fields = []
    ordering_fields = ["id", "created_at", "estimated_cost", "consent_signed"]
