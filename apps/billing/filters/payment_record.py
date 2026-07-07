import django_filters

from apps.billing.models import PaymentRecord


class PaymentRecordFilter(django_filters.FilterSet):
    created_at = django_filters.DateFromToRangeFilter()
    amount_min = django_filters.NumberFilter(field_name="amount", lookup_expr="gte")
    amount_max = django_filters.NumberFilter(field_name="amount", lookup_expr="lte")

    class Meta:
        model = PaymentRecord
        fields = ["invoice", "method", "gateway_status"]
