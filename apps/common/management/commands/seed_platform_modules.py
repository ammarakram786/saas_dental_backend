"""Seed canonical PlatformModule catalog rows."""
from django.core.management.base import BaseCommand

from apps.platform.models import PlatformModule

DEFAULT_MODULES = [
    {
        "codename": "manage_tenants",
        "name": "Manage Tenants",
        "description": "Provision and manage customer organizations.",
    },
    {
        "codename": "manage_billing",
        "name": "Manage Billing",
        "description": "Cross-tenant billing and invoice overview.",
    },
    {
        "codename": "manage_support",
        "name": "Manage Support",
        "description": "Operational health and customer support (reserved).",
    },
    {
        "codename": "security_audit",
        "name": "Security Audit",
        "description": "Chronological log of sensitive operations.",
    },
]


class Command(BaseCommand):
    help = "Idempotently seed PlatformModule catalog entries."

    def handle(self, *args, **options):
        created = 0
        for row in DEFAULT_MODULES:
            _, was_created = PlatformModule.objects.update_or_create(
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
                f"Platform modules ready ({created} created, "
                f"{len(DEFAULT_MODULES) - created} updated)."
            )
        )
