from apps.appointments.filters import AppointmentFilter
from apps.appointments.models import Appointment
from apps.appointments.serializers import AppointmentSerializer
from apps.common.viewsets import BaseTenantViewSet


class AppointmentViewSet(BaseTenantViewSet):
    queryset = Appointment.objects.select_related("patient", "slot")
    serializer_class = AppointmentSerializer
    required_tenant_permission = "manage_appointments"

    filterset_class = AppointmentFilter
    search_fields = ["patient__username", "appointment_type", "notes"]
    ordering_fields = ["id", "created_at", "status", "appointment_type"]
