"""Seed canonical TenantPermission catalog rows."""
from django.core.management.base import BaseCommand

from apps.tenants.models import TenantPermission

DEFAULT_PERMISSIONS = [
    {
        "codename": "manage_members",
        "name": "Manage Members",
        "description": "Invite and manage tenant memberships and roles.",
    },
    {
        "codename": "manage_appointments",
        "name": "Manage Appointments",
        "description": "Create and manage appointments, slots, and clinic assets.",
    },
    {
        "codename": "view_appointments",
        "name": "View Appointments",
        "description": "View the clinic schedule.",
    },
    {
        "codename": "view_reports",
        "name": "View Reports",
        "description": "View clinic operational reports.",
    },
    {
        "codename": "edit_clinical_chart",
        "name": "Edit Clinical Chart",
        "description": "Create and edit odontograms, notes, and prescriptions.",
    },
    {
        "codename": "manage_treatment_plans",
        "name": "Manage Treatment Plans",
        "description": "Create and manage treatment plans.",
    },
    {
        "codename": "manage_billing",
        "name": "Manage Billing",
        "description": "Manage invoices, payments, and insurance panels.",
    },
]


class Command(BaseCommand):
    help = "Idempotently seed TenantPermission catalog entries."

    def handle(self, *args, **options):
        created = 0
        for row in DEFAULT_PERMISSIONS:
            _, was_created = TenantPermission.objects.update_or_create(
                codename=row["codename"],
                defaults={
                    "name": row["name"],
                    "description": row["description"],
                    "is_active": True,
                },
            )
            if was_created:
                created += 1
        self.stdout.write(
            self.style.SUCCESS(
                f"Tenant permissions ready ({created} created, "
                f"{len(DEFAULT_PERMISSIONS) - created} updated)."
            )
        )
