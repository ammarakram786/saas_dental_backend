from apps.billing.filters import PaymentRecordFilter
from apps.billing.models import PaymentRecord
from apps.billing.serializers import PaymentRecordSerializer
from apps.common.viewsets import BaseTenantViewSet


class PaymentRecordViewSet(BaseTenantViewSet):
    queryset = PaymentRecord.objects.select_related("invoice")
    serializer_class = PaymentRecordSerializer
    required_tenant_permission = "manage_billing"

    filterset_class = PaymentRecordFilter
    search_fields = ["gateway_ref"]
    ordering_fields = ["id", "created_at", "amount", "method"]
