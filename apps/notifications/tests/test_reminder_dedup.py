from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import TestCase
from django.utils import timezone

from apps.accounts.models import PatientUserProfile
from apps.appointments.models import Appointment, AppointmentSlot, ClinicAsset
from apps.notifications.tasks.appointment_notifications import (
    _reminder_cache_key,
    send_due_appointment_reminders,
)
from apps.tenants.models import Tenant

User = get_user_model()


class ReminderDedupTests(TestCase):
    def setUp(self):
        cache.clear()
        self.tenant = Tenant.objects.create(name="Remind", slug="remind")
        dentist = User.objects.create_user(username="rdent", password="x")
        patient = User.objects.create_user(username="rpat", password="x")
        PatientUserProfile.objects.create(user=patient, primary_phone="+92111")
        chair = ClinicAsset.objects.create(
            tenant=self.tenant, name="C1", asset_type="chair"
        )
        start = timezone.now() + timedelta(hours=12)
        slot = AppointmentSlot.objects.create(
            tenant=self.tenant,
            dentist=dentist,
            chair=chair,
            start_time=start,
            end_time=start + timedelta(minutes=30),
            is_available=False,
        )
        self.appointment = Appointment.objects.create(
            tenant=self.tenant,
            patient=patient,
            slot=slot,
            status="confirmed",
            appointment_type="checkup",
        )

    def test_second_run_skips_dedup(self):
        first = send_due_appointment_reminders()
        self.assertEqual(first["sent"], 1)
        self.assertTrue(cache.get(_reminder_cache_key(self.appointment.pk)))
        second = send_due_appointment_reminders()
        self.assertEqual(second["sent"], 0)
        self.assertEqual(second["skipped_dedup"], 1)
