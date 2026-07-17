from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.appointments.filters import AppointmentFilter
from apps.appointments.models import Appointment
from apps.appointments.serializers import AppointmentSerializer
from apps.appointments.services.booking import (
    BookingError,
    book_slot_for_patient,
    cancel_patient_appointment,
)


class PatientAppointmentViewSet(ModelViewSet):
    """Patient-facing appointments: list/retrieve + book/cancel actions."""

    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "head", "options"]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = AppointmentFilter
    search_fields = ["appointment_type", "notes"]
    ordering_fields = ["id", "created_at", "status", "appointment_type"]

    def get_queryset(self):
        return Appointment.objects.select_related("tenant", "slot").filter(
            patient=self.request.user
        )

    def create(self, request, *args, **kwargs):
        return Response(
            {"detail": "Use POST /api/scheduling/patient/book/ to book a slot."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    @action(detail=False, methods=["post"], url_path="book")
    def book(self, request):
        slot_id = request.data.get("slot")
        appointment_type = request.data.get("appointment_type") or "checkup"
        notes = request.data.get("notes") or ""
        if not slot_id:
            return Response(
                {"slot": ["This field is required."]},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            appointment = book_slot_for_patient(
                patient=request.user,
                slot_id=int(slot_id),
                appointment_type=appointment_type,
                notes=notes,
            )
        except BookingError as exc:
            return Response(exc.detail, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            AppointmentSerializer(appointment).data,
            status=status.HTTP_201_CREATED,
        )

    @action(detail=True, methods=["post"], url_path="cancel")
    def cancel(self, request, pk=None):
        try:
            appointment = cancel_patient_appointment(
                patient=request.user,
                appointment_id=int(pk),
            )
        except BookingError as exc:
            return Response(exc.detail, status=status.HTTP_400_BAD_REQUEST)
        return Response(AppointmentSerializer(appointment).data)
