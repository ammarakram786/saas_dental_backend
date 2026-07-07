import django_filters

from apps.appointments.models import Appointment


class AppointmentFilter(django_filters.FilterSet):
    appointment_type = django_filters.CharFilter(lookup_expr="icontains")
    created_at = django_filters.DateFromToRangeFilter()
    slot_start_after = django_filters.DateTimeFilter(
        field_name="slot__start_time", lookup_expr="gte"
    )
    slot_start_before = django_filters.DateTimeFilter(
        field_name="slot__start_time", lookup_expr="lte"
    )

    class Meta:
        model = Appointment
        fields = ["patient", "status", "slot"]
