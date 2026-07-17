from __future__ import annotations

from datetime import timedelta

from celery import shared_task
from django.core.cache import cache
from django.utils import timezone

from apps.appointments.models import Appointment
from apps.notifications.adapters import SmsGatewayFactory

REMINDER_DEDUP_TTL = 60 * 60 * 20  # 20 hours


def _patient_phone(appointment: Appointment) -> str:
    profile = getattr(appointment.patient, "patient_profile", None)
    return getattr(profile, "primary_phone", "")


def _reminder_cache_key(appointment_id: int) -> str:
    return f"appt:reminder:sent:{appointment_id}"


@shared_task
def send_appointment_confirmation(appointment_id: int):
    appointment = Appointment.objects.select_related("patient", "tenant").get(pk=appointment_id)
    phone = _patient_phone(appointment)
    if not phone:
        return {"status": "skipped", "reason": "no_phone"}
    return SmsGatewayFactory.get().send_sms(
        to=phone,
        message=f"Your appointment at {appointment.tenant.name} is confirmed.",
    )


@shared_task
def send_schedule_change(appointment_id: int):
    appointment = Appointment.objects.select_related("patient", "tenant").get(pk=appointment_id)
    phone = _patient_phone(appointment)
    if not phone:
        return {"status": "skipped", "reason": "no_phone"}
    return SmsGatewayFactory.get().send_sms(
        to=phone,
        message=f"Your appointment at {appointment.tenant.name} was updated.",
    )


@shared_task
def send_due_appointment_reminders():
    now = timezone.now()
    soon = now + timedelta(hours=24)
    count = 0
    skipped = 0
    for appointment in Appointment.objects.select_related("slot", "tenant", "patient").filter(
        status="confirmed",
        slot__start_time__gte=now,
        slot__start_time__lte=soon,
    ):
        key = _reminder_cache_key(appointment.pk)
        if cache.get(key):
            skipped += 1
            continue
        phone = _patient_phone(appointment)
        if not phone:
            continue
        SmsGatewayFactory.get().send_sms(
            to=phone,
            message=f"Reminder: appointment tomorrow at {appointment.tenant.name}.",
        )
        cache.set(key, True, REMINDER_DEDUP_TTL)
        count += 1
    return {"sent": count, "skipped_dedup": skipped}
