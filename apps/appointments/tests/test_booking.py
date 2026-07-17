from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from apps.accounts.models import PatientUserProfile
from apps.appointments.models import AppointmentSlot, ClinicAsset
from apps.appointments.services.booking import (
    BookingError,
    book_slot_for_patient,
    cancel_patient_appointment,
)
from apps.tenants.models import Tenant, TenantPermission

User = get_user_model()


class BookingServiceTests(TestCase):
    def setUp(self):
        TenantPermission.objects.get_or_create(
            codename="manage_appointments",
            defaults={"name": "Manage Appointments"},
        )
        self.tenant = Tenant.objects.create(name="Clinic", slug="clinic")
        self.dentist = User.objects.create_user(username="dentist", password="x")
        self.patient = User.objects.create_user(username="patient", password="x")
        PatientUserProfile.objects.create(user=self.patient, primary_phone="+92000")
        self.chair = ClinicAsset.objects.create(
            tenant=self.tenant, name="Chair 1", asset_type="chair"
        )
        start = timezone.now() + timedelta(hours=2)
        self.slot = AppointmentSlot.objects.create(
            tenant=self.tenant,
            dentist=self.dentist,
            chair=self.chair,
            start_time=start,
            end_time=start + timedelta(minutes=30),
            is_available=True,
        )

    def test_book_reserves_slot(self):
        appointment = book_slot_for_patient(
            patient=self.patient,
            slot_id=self.slot.pk,
            appointment_type="checkup",
        )
        self.slot.refresh_from_db()
        self.assertFalse(self.slot.is_available)
        self.assertEqual(appointment.status, "confirmed")
        self.assertEqual(appointment.patient_id, self.patient.pk)

    def test_double_book_raises(self):
        book_slot_for_patient(patient=self.patient, slot_id=self.slot.pk)
        other = User.objects.create_user(username="other", password="x")
        with self.assertRaises(BookingError):
            book_slot_for_patient(patient=other, slot_id=self.slot.pk)

    def test_cancel_releases_slot(self):
        appointment = book_slot_for_patient(patient=self.patient, slot_id=self.slot.pk)
        cancel_patient_appointment(patient=self.patient, appointment_id=appointment.pk)
        self.slot.refresh_from_db()
        appointment.refresh_from_db()
        self.assertEqual(appointment.status, "cancelled")
        self.assertTrue(self.slot.is_available)


class PatientBookingAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.tenant = Tenant.objects.create(name="Clinic", slug="clinic-api")
        self.dentist = User.objects.create_user(username="dentist2", password="x")
        self.patient = User.objects.create_user(username="patient2", password="x")
        PatientUserProfile.objects.create(user=self.patient)
        chair = ClinicAsset.objects.create(
            tenant=self.tenant, name="Chair A", asset_type="chair"
        )
        start = timezone.now() + timedelta(hours=3)
        self.slot = AppointmentSlot.objects.create(
            tenant=self.tenant,
            dentist=self.dentist,
            chair=chair,
            start_time=start,
            end_time=start + timedelta(minutes=30),
            is_available=True,
        )
        self.client.force_authenticate(user=self.patient)

    def test_book_and_cancel_endpoints(self):
        book = self.client.post(
            "/api/scheduling/patient/book/",
            {"slot": self.slot.pk, "appointment_type": "cleaning"},
            format="json",
        )
        self.assertEqual(book.status_code, status.HTTP_201_CREATED)
        appt_id = book.data["id"]

        cancel = self.client.post(f"/api/scheduling/patient/{appt_id}/cancel/")
        self.assertEqual(cancel.status_code, status.HTTP_200_OK)
        self.assertEqual(cancel.data["status"], "cancelled")
