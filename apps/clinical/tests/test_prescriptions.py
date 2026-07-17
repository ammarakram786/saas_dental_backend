from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from apps.appointments.models import Appointment, AppointmentSlot, ClinicAsset
from apps.clinical.models import ClinicalNote, Prescription
from apps.tenants.models import Tenant, TenantMembership, TenantPermission, TenantRole
from apps.tenants.services import seed_default_roles

User = get_user_model()


class PrescriptionAPITests(TestCase):
    def setUp(self):
        for codename, name in [
            ("edit_clinical_chart", "Edit Clinical Chart"),
            ("manage_appointments", "Manage Appointments"),
        ]:
            TenantPermission.objects.get_or_create(
                codename=codename, defaults={"name": name}
            )

        self.tenant = Tenant.objects.create(name="Clinic", slug="rx-clinic")
        seed_default_roles(self.tenant)

        self.dentist = User.objects.create_user(username="rxdentist", password="x")
        role = TenantRole.objects.get(tenant=self.tenant, slug="admin")
        TenantMembership.objects.create(
            user=self.dentist, tenant=self.tenant, role=role, is_active=True
        )

        patient = User.objects.create_user(username="rxpatient", password="x")
        chair = ClinicAsset.objects.create(
            tenant=self.tenant, name="Chair", asset_type="chair"
        )
        start = timezone.now() + timedelta(hours=1)
        slot = AppointmentSlot.objects.create(
            tenant=self.tenant,
            dentist=self.dentist,
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
        self.note = ClinicalNote.objects.create(
            tenant=self.tenant,
            appointment=self.appointment,
            dentist=self.dentist,
            body="Exam note",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.dentist)
        self.client.credentials(HTTP_X_TENANT_ID=str(self.tenant.pk))

    def test_create_prescription(self):
        response = self.client.post(
            "/api/clinical/prescriptions/",
            {
                "clinical_note": self.note.pk,
                "medications": [{"name": "Amox", "dose": "500mg"}],
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Prescription.objects.filter(tenant=self.tenant).count(), 1)
