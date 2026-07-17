"""Atomic appointment booking helpers."""
from __future__ import annotations

from django.db import transaction

from apps.appointments.models import Appointment, AppointmentSlot


class BookingError(Exception):
    def __init__(self, detail: dict | str):
        self.detail = detail if isinstance(detail, dict) else {"detail": detail}
        super().__init__(str(detail))


@transaction.atomic
def book_slot_for_patient(
    *,
    patient,
    slot_id: int,
    appointment_type: str = "checkup",
    notes: str = "",
) -> Appointment:
    try:
        slot = (
            AppointmentSlot.objects.select_for_update()
            .select_related("tenant")
            .get(pk=slot_id)
        )
    except AppointmentSlot.DoesNotExist as exc:
        raise BookingError({"slot": ["Slot not found."]}) from exc

    if not slot.is_available:
        raise BookingError({"slot": ["Slot is no longer available."]})
    if not slot.tenant.is_active:
        raise BookingError({"slot": ["Clinic is not accepting bookings."]})

    slot.is_available = False
    slot.save(update_fields=["is_available"])

    return Appointment.objects.create(
        tenant=slot.tenant,
        patient=patient,
        slot=slot,
        status="confirmed",
        appointment_type=appointment_type,
        notes=notes,
    )


@transaction.atomic
def cancel_patient_appointment(*, patient, appointment_id: int) -> Appointment:
    try:
        appointment = (
            Appointment.objects.select_for_update()
            .select_related("slot")
            .get(pk=appointment_id, patient=patient)
        )
    except Appointment.DoesNotExist as exc:
        raise BookingError({"detail": "Appointment not found."}) from exc

    if appointment.status == "cancelled":
        raise BookingError({"detail": "Appointment is already cancelled."})
    if appointment.status == "completed":
        raise BookingError({"detail": "Completed appointments cannot be cancelled."})

    appointment.status = "cancelled"
    appointment.save(update_fields=["status"])

    slot = appointment.slot
    if not Appointment.objects.filter(
        slot=slot,
        status__in=["pending", "confirmed", "arrived"],
    ).exclude(pk=appointment.pk).exists():
        slot.is_available = True
        slot.save(update_fields=["is_available"])

    return appointment
