import django_filters

from apps.clinical.models import Odontogram


class OdontogramFilter(django_filters.FilterSet):
    patient = django_filters.NumberFilter(field_name="appointment__patient_id")
    created_at = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Odontogram
        fields = ["appointment"]
