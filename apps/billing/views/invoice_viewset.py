from apps.billing.filters import InvoiceFilter
from apps.billing.models import Invoice
from apps.billing.serializers import InvoiceSerializer
from apps.common.viewsets import BaseTenantViewSet


class InvoiceViewSet(BaseTenantViewSet):
    queryset = Invoice.objects.select_related("appointment", "patient")
    serializer_class = InvoiceSerializer
    required_tenant_permission = "manage_billing"

    filterset_class = InvoiceFilter
    search_fields = ["patient__username", "patient__email"]
    ordering_fields = ["id", "created_at", "subtotal", "copay_amount", "status"]
