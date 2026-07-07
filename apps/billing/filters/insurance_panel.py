import django_filters

from apps.billing.models import InsurancePanel


class InsurancePanelFilter(django_filters.FilterSet):
    insurer_name = django_filters.CharFilter(lookup_expr="icontains")
    panel_code = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = InsurancePanel
        fields = ["panel_code"]
