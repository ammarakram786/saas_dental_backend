import django_filters

from apps.clinical.models import TreatmentPlan


class TreatmentPlanFilter(django_filters.FilterSet):
    patient = django_filters.NumberFilter(field_name="appointment__patient_id")
    created_at = django_filters.DateFromToRangeFilter()
    estimated_cost_min = django_filters.NumberFilter(
        field_name="estimated_cost", lookup_expr="gte"
    )
    estimated_cost_max = django_filters.NumberFilter(
        field_name="estimated_cost", lookup_expr="lte"
    )

    class Meta:
        model = TreatmentPlan
        fields = ["appointment", "consent_signed"]
