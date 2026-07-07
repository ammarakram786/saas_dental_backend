import django_filters

from apps.billing.models import Invoice


class InvoiceFilter(django_filters.FilterSet):
    created_at = django_filters.DateFromToRangeFilter()
    subtotal_min = django_filters.NumberFilter(field_name="subtotal", lookup_expr="gte")
    subtotal_max = django_filters.NumberFilter(field_name="subtotal", lookup_expr="lte")
    copay_amount_min = django_filters.NumberFilter(field_name="copay_amount", lookup_expr="gte")
    copay_amount_max = django_filters.NumberFilter(field_name="copay_amount", lookup_expr="lte")

    class Meta:
        model = Invoice
        fields = ["status", "patient", "appointment", "tenant"]
