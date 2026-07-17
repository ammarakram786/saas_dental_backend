from django.core.management import call_command
from django.test import TestCase

from apps.platform.models import PlatformModule
from apps.tenants.models import Tenant, TenantPermission


class SeedCommandTests(TestCase):
    def test_seed_permissions_and_modules(self):
        call_command("seed_permissions")
        call_command("seed_platform_modules")
        self.assertTrue(TenantPermission.objects.filter(codename="manage_appointments").exists())
        self.assertTrue(PlatformModule.objects.filter(codename="manage_tenants").exists())

    def test_create_demo_clinic(self):
        call_command("create_demo_clinic")
        self.assertTrue(Tenant.objects.filter(slug="demo-clinic").exists())
        # Idempotent re-run
        call_command("create_demo_clinic")
        self.assertEqual(Tenant.objects.filter(slug="demo-clinic").count(), 1)
