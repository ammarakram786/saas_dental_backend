from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.appointments.filters import AppointmentFilter
from apps.appointments.models import Appointment
from apps.appointments.serializers import AppointmentSerializer


class PatientAppointmentViewSet(ReadOnlyModelViewSet):
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = AppointmentFilter
    search_fields = ["patient__username", "appointment_type", "notes"]
    ordering_fields = ["id", "created_at", "status", "appointment_type"]

    def get_queryset(self):
        return Appointment.objects.select_related("tenant", "slot").filter(
            patient=self.request.user
        )
