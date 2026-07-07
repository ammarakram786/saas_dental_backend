from apps.billing.filters import InsurancePanelFilter
from apps.billing.models import InsurancePanel
from apps.billing.serializers import InsurancePanelSerializer
from apps.common.viewsets import BaseTenantViewSet


class InsurancePanelViewSet(BaseTenantViewSet):
    queryset = InsurancePanel.objects.all()
    serializer_class = InsurancePanelSerializer
    required_tenant_permission = "manage_billing"

    filterset_class = InsurancePanelFilter
    search_fields = ["insurer_name", "panel_code"]
    ordering_fields = ["id", "insurer_name", "panel_code", "created_at"]
