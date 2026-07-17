"""Create a demo clinic with staff, patient, slots, appointments, and invoices."""
from __future__ import annotations

from datetime import timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from apps.accounts.models import PatientUserProfile, PlatformUserProfile
from apps.appointments.models import Appointment, AppointmentSlot, ClinicAsset
from apps.billing.models import Invoice, PaymentRecord
from apps.platform.models import PlatformModule, PlatformRole
from apps.tenants.models import Tenant, TenantMembership, TenantRole
from apps.tenants.services import provision_tenant_with_admin, seed_default_roles

User = get_user_model()

DEMO_PASSWORD = "DemoPass123!"


class Command(BaseCommand):
    help = (
        "Seed permissions/modules and create a demo clinic with sample data. "
        f"All demo passwords are '{DEMO_PASSWORD}'."
    )

    @transaction.atomic
    def handle(self, *args, **options):
        call_command("seed_permissions")
        call_command("seed_platform_modules")

        platform_admin, _ = User.objects.get_or_create(
            username="platform.admin",
            defaults={
                "email": "platform@dentaldoodle.pk",
                "first_name": "Platform",
                "last_name": "Admin",
                "is_staff": True,
                "is_superuser": True,
            },
        )
        platform_admin.set_password(DEMO_PASSWORD)
        platform_admin.save()

        role, _ = PlatformRole.objects.get_or_create(
            slug="platform-admin",
            defaults={
                "name": "Platform Administrator",
                "description": "Full platform access.",
                "is_active": True,
            },
        )
        role.modules.set(PlatformModule.objects.filter(is_active=True))
        PlatformUserProfile.objects.update_or_create(
            user=platform_admin,
            defaults={"role": role, "is_super_admin": True},
        )

        tenant = Tenant.objects.filter(slug="demo-clinic").first()
        if tenant is None:
            result = provision_tenant_with_admin(
                name="Demo Dental Clinic",
                slug="demo-clinic",
                admin_email="admin@demo-clinic.pk",
                admin_first_name="Clinic",
                admin_last_name="Admin",
                admin_password=DEMO_PASSWORD,
            )
            tenant = result.tenant
            clinic_admin = result.admin_user
        else:
            seed_default_roles(tenant)
            clinic_admin = User.objects.get(email__iexact="admin@demo-clinic.pk")

        staff_user, _ = User.objects.get_or_create(
            username="demo.staff",
            defaults={
                "email": "staff@demo-clinic.pk",
                "first_name": "Demo",
                "last_name": "Staff",
            },
        )
        staff_user.set_password(DEMO_PASSWORD)
        staff_user.save()
        manager_role = TenantRole.objects.get(tenant=tenant, slug="manager")
        TenantMembership.objects.get_or_create(
            user=staff_user,
            tenant=tenant,
            defaults={"role": manager_role, "is_active": True},
        )

        patient_user, _ = User.objects.get_or_create(
            username="demo.patient",
            defaults={
                "email": "patient@example.com",
                "first_name": "Demo",
                "last_name": "Patient",
            },
        )
        patient_user.set_password(DEMO_PASSWORD)
        patient_user.save()
        PatientUserProfile.objects.get_or_create(
            user=patient_user,
            defaults={"primary_phone": "+923001234567", "blood_type": "O+"},
        )

        chair, _ = ClinicAsset.objects.get_or_create(
            tenant=tenant,
            name="Chair 1",
            defaults={"asset_type": "chair", "is_operational": True},
        )

        now = timezone.now().replace(minute=0, second=0, microsecond=0)
        slots = []
        for hour_offset in (2, 4, 6, 26, 28):
            start = now + timedelta(hours=hour_offset)
            end = start + timedelta(minutes=30)
            slot, _ = AppointmentSlot.objects.get_or_create(
                tenant=tenant,
                dentist=clinic_admin,
                chair=chair,
                start_time=start,
                defaults={"end_time": end, "is_available": True},
            )
            slots.append(slot)

        booked = slots[0]
        appointment, _ = Appointment.objects.get_or_create(
            tenant=tenant,
            patient=patient_user,
            slot=booked,
            defaults={
                "status": "confirmed",
                "appointment_type": "checkup",
                "notes": "Demo checkup appointment",
            },
        )
        if booked.is_available:
            booked.is_available = False
            booked.save(update_fields=["is_available"])

        invoice, _ = Invoice.objects.get_or_create(
            tenant=tenant,
            patient=patient_user,
            appointment=appointment,
            defaults={
                "status": "issued",
                "line_items": [
                    {"description": "Consultation", "amount": "2500.00"},
                ],
                "subtotal": Decimal("2500.00"),
                "copay_amount": Decimal("500.00"),
                "insurance_coverage": Decimal("2000.00"),
            },
        )
        PaymentRecord.objects.get_or_create(
            tenant=tenant,
            invoice=invoice,
            defaults={
                "amount": Decimal("500.00"),
                "method": "cash",
                "gateway_status": "manual",
            },
        )

        self.stdout.write(self.style.SUCCESS("Demo clinic ready."))
        self.stdout.write(f"  Platform admin: platform.admin / {DEMO_PASSWORD}")
        self.stdout.write(f"  Clinic admin:   admin@demo-clinic.pk / {DEMO_PASSWORD}")
        self.stdout.write(f"  Clinic staff:   staff@demo-clinic.pk / {DEMO_PASSWORD}")
        self.stdout.write(f"  Patient:        patient@example.com / {DEMO_PASSWORD}")
        self.stdout.write("  Tenant slug:    demo-clinic")
