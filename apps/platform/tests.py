from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate

from apps.common.viewsets import BasePlatformViewSet
from apps.platform.models import PlatformModule, PlatformRole

User = get_user_model()


class BillingViewSet(BasePlatformViewSet):
    required_module_codename = "manage_billing"
    queryset = PlatformModule.objects.all()

    def list(self, request, *args, **kwargs):
        from rest_framework.response import Response

        return Response({"ok": True})


class HasPlatformModuleAccessTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        # manage_billing is seeded by migration; ensure it exists regardless.
        self.module, _ = PlatformModule.objects.get_or_create(
            codename="manage_billing", defaults={"name": "Manage Billing"}
        )
        self.view = BillingViewSet.as_view({"get": "list"})

    def _get(self, user):
        request = self.factory.get("/platform/billing/")
        force_authenticate(request, user=user)
        return self.view(request)

    def test_user_without_role_is_denied(self):
        user = User.objects.create_user(username="plain", password="x")
        self.assertEqual(self._get(user).status_code, 403)

    def test_user_with_role_lacking_module_is_denied(self):
        role = PlatformRole.objects.create(name="Support", slug="support")
        user = User.objects.create_user(
            username="support", password="x", platform_role=role
        )
        self.assertEqual(self._get(user).status_code, 403)

    def test_user_with_role_granting_module_is_allowed(self):
        role = PlatformRole.objects.create(name="Billing", slug="billing")
        role.modules.add(self.module)
        user = User.objects.create_user(
            username="biller", password="x", platform_role=role
        )
        self.assertEqual(self._get(user).status_code, 200)

    def test_super_admin_bypasses_module_check(self):
        user = User.objects.create_user(
            username="root", password="x", is_super_admin=True
        )
        self.assertEqual(self._get(user).status_code, 200)

    def test_inactive_role_is_denied(self):
        role = PlatformRole.objects.create(
            name="Billing2", slug="billing2", is_active=False
        )
        role.modules.add(self.module)
        user = User.objects.create_user(
            username="biller2", password="x", platform_role=role
        )
        self.assertEqual(self._get(user).status_code, 403)
