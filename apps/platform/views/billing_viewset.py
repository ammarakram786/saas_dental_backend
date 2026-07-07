from apps.billing.filters import InvoiceFilter
from apps.billing.models import Invoice
from apps.common.viewsets import BasePlatformViewSet
from apps.platform.serializers import PlatformBillingSerializer


class BillingViewSet(BasePlatformViewSet):
    queryset = Invoice.objects.select_related("tenant", "patient").all()
    serializer_class = PlatformBillingSerializer
    required_module_codename = "manage_billing"

    filterset_class = InvoiceFilter
    search_fields = ["tenant__name", "patient__username"]
    ordering_fields = ["id", "created_at", "subtotal", "copay_amount"]
