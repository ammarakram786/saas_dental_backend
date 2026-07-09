from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient, APIRequestFactory, force_authenticate

from apps.accounts.models import PlatformUserProfile
from apps.common.viewsets import BasePlatformViewSet
from apps.platform.models import PlatformModule, PlatformRole
from apps.tenants.models import Tenant, TenantMembership, TenantPermission, TenantRole

User = get_user_model()


class BillingViewSet(BasePlatformViewSet):
    required_module_codename = "manage_billing"
    queryset = PlatformModule.objects.all()

    def list(self, request, *args, **kwargs):
        from rest_framework.response import Response

        return Response({"ok": True})


def _create_platform_user(username, password, *, role=None, is_super_admin=False):
    user = User.objects.create_user(username=username, password=password)
    PlatformUserProfile.objects.create(
        user=user,
        role=role,
        is_super_admin=is_super_admin,
    )
    return user


class HasPlatformModuleAccessTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
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
        user = _create_platform_user("support", "x", role=role)
        self.assertEqual(self._get(user).status_code, 403)

    def test_user_with_role_granting_module_is_allowed(self):
        role = PlatformRole.objects.create(name="Billing", slug="billing")
        role.modules.add(self.module)
        user = _create_platform_user("biller", "x", role=role)
        self.assertEqual(self._get(user).status_code, 200)

    def test_super_admin_bypasses_module_check(self):
        user = User.objects.create_superuser(
            username="root",
            password="x",
            email="root@test.com",
        )
        self.assertTrue(PlatformUserProfile.objects.filter(user=user, is_super_admin=True).exists())
        self.assertEqual(self._get(user).status_code, 200)

    def test_inactive_role_is_denied(self):
        role = PlatformRole.objects.create(
            name="Billing2", slug="billing2", is_active=False
        )
        role.modules.add(self.module)
        user = _create_platform_user("biller2", "x", role=role)
        self.assertEqual(self._get(user).status_code, 403)


class TenantCreateViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.operator = _create_tenant_operator()
        self.client.force_authenticate(user=self.operator)
        self.url = "/api/platform/tenants/"

    def test_create_tenant_provisions_admin_user(self):
        response = self.client.post(
            self.url,
            {
                "name": "Acme Dental",
                "slug": "acme",
                "is_active": True,
                "admin_user": {
                    "email": "admin@acme.com",
                    "first_name": "Jane",
                    "last_name": "Admin",
                    "password": "securepass",
                },
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Acme Dental")
        self.assertEqual(response.data["slug"], "acme")
        self.assertTrue(response.data["admin_user"]["created"])
        self.assertEqual(response.data["admin_user"]["email"], "admin@acme.com")

        tenant = Tenant.objects.get(slug="acme")
        admin_user = User.objects.get(email="admin@acme.com")
        membership = TenantMembership.objects.get(user=admin_user, tenant=tenant)
        admin_role = TenantRole.objects.get(tenant=tenant, slug="admin")

        self.assertEqual(membership.role_id, admin_role.id)
        all_codenames = set(
            TenantPermission.objects.filter(is_active=True).values_list("codename", flat=True)
        )
        self.assertEqual(admin_role.permission_codenames(), all_codenames)

    def test_create_tenant_assigns_existing_user_as_admin(self):
        existing = User.objects.create_user(
            username="existing",
            email="existing@acme.com",
            password="oldpass12",
            first_name="Existing",
            last_name="User",
        )

        response = self.client.post(
            self.url,
            {
                "name": "Beta Clinic",
                "slug": "beta",
                "admin_user": {
                    "email": "existing@acme.com",
                },
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertFalse(response.data["admin_user"]["created"])
        self.assertEqual(response.data["admin_user"]["id"], existing.pk)

        tenant = Tenant.objects.get(slug="beta")
        membership = TenantMembership.objects.get(user=existing, tenant=tenant)
        self.assertEqual(membership.role.slug, "admin")

    def test_create_tenant_requires_admin_user(self):
        response = self.client.post(
            self.url,
            {"name": "No Admin", "slug": "no-admin"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("admin_user", response.data)

    def test_create_tenant_requires_password_for_new_user(self):
        response = self.client.post(
            self.url,
            {
                "name": "Gamma",
                "slug": "gamma",
                "admin_user": {"email": "new@gamma.com"},
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("admin_user", response.data)

    def test_create_tenant_rolls_back_on_invalid_slug(self):
        Tenant.objects.create(name="Taken", slug="taken")

        response = self.client.post(
            self.url,
            {
                "name": "Another",
                "slug": "taken",
                "admin_user": {
                    "email": "admin@another.com",
                    "password": "securepass",
                },
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(User.objects.filter(email="admin@another.com").exists())


def _create_tenant_operator(username="operator", password="pass1234"):
    module, _ = PlatformModule.objects.get_or_create(
        codename="manage_tenants",
        defaults={"name": "Manage Tenants"},
    )
    role = PlatformRole.objects.create(name="Tenant Ops", slug="tenant-ops")
    role.modules.add(module)
    user = User.objects.create_user(username=username, password=password, email=f"{username}@test.com")
    PlatformUserProfile.objects.create(user=user, role=role)
    return user
