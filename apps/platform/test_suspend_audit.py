from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from apps.accounts.models import PlatformUserProfile
from apps.platform.models import PlatformAuditEvent, PlatformModule, PlatformRole
from apps.tenants.models import Tenant

User = get_user_model()


class TenantSuspendAuditTests(TestCase):
    def setUp(self):
        module, _ = PlatformModule.objects.get_or_create(
            codename="manage_tenants", defaults={"name": "Manage Tenants"}
        )
        role = PlatformRole.objects.create(name="Ops", slug="ops")
        role.modules.add(module)
        self.user = User.objects.create_user(username="ops", password="x")
        PlatformUserProfile.objects.create(user=self.user, role=role)
        self.tenant = Tenant.objects.create(name="Suspend Me", slug="suspend-me", is_active=True)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_suspend_writes_audit_event(self):
        response = self.client.patch(
            f"/api/platform/tenants/{self.tenant.pk}/",
            {"is_active": False},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            PlatformAuditEvent.objects.filter(
                action="suspended tenant", target="suspend-me"
            ).exists()
        )


class OpenAPISchemaTests(TestCase):
    def test_schema_endpoint_available_in_test(self):
        client = APIClient()
        response = client.get("/api/schema/")
        # Schema may require auth depending on settings; accept 200 or 401/403
        self.assertIn(response.status_code, (200, 401, 403))
