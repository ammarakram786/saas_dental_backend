from apps.appointments.models import AppointmentSlot
from apps.appointments.serializers import AppointmentSlotSerializer
from apps.common.viewsets import BaseTenantViewSet
import django_filters


class AppointmentSlotFilter(django_filters.FilterSet):
    class Meta:
        model = AppointmentSlot
        fields = ["dentist", "chair", "is_available"]


class AppointmentSlotViewSet(BaseTenantViewSet):
    queryset = AppointmentSlot.objects.select_related("dentist", "chair")
    serializer_class = AppointmentSlotSerializer
    required_tenant_permission = "manage_appointments"

    filterset_class = AppointmentSlotFilter
    search_fields = ["dentist__username"]
    ordering_fields = ["id", "start_time", "end_time", "is_available"]
