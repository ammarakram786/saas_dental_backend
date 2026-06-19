from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory, force_authenticate

from apps.common.viewsets import BaseTenantViewSet
from apps.tenants.models import Tenant, TenantMembership, TenantRole

User = get_user_model()


class _TenantRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantRole
        fields = ("id", "name", "slug")


class _IsolationViewSet(BaseTenantViewSet):
    """Lists TenantRole rows (themselves TenantResources) to prove isolation."""

    serializer_class = _TenantRoleSerializer
    queryset = TenantRole.objects.all()
    pagination_class = None


class _ManageMembersViewSet(BaseTenantViewSet):
    serializer_class = _TenantRoleSerializer
    queryset = TenantRole.objects.all()
    pagination_class = None
    required_tenant_permission = "manage_members"

    def list(self, request, *args, **kwargs):
        return Response({"ok": True})


def _add_member(user, tenant, role_slug):
    role = TenantRole.objects.get(tenant=tenant, slug=role_slug)
    return TenantMembership.objects.create(user=user, tenant=tenant, role=role)


class TenantIsolationTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.tenant_a = Tenant.objects.create(name="A", slug="a")
        self.tenant_b = Tenant.objects.create(name="B", slug="b")
        self.user = User.objects.create_user(username="u", password="x")
        _add_member(self.user, self.tenant_a, "admin")
        self.view = _IsolationViewSet.as_view({"get": "list"})

    def _list_for_tenant(self, tenant):
        request = self.factory.get("/roles/")
        force_authenticate(request, user=self.user)
        request.tenant = tenant
        return self.view(request)

    def test_queryset_only_returns_active_tenant_rows(self):
        response = self._list_for_tenant(self.tenant_a)
        self.assertEqual(response.status_code, 200)
        returned_ids = {row["id"] for row in response.data}
        expected_ids = set(
            TenantRole.objects.filter(tenant=self.tenant_a).values_list(
                "id", flat=True
            )
        )
        self.assertEqual(returned_ids, expected_ids)
        tenant_b_ids = set(
            TenantRole.objects.filter(tenant=self.tenant_b).values_list(
                "id", flat=True
            )
        )
        self.assertTrue(returned_ids.isdisjoint(tenant_b_ids))

    def test_missing_tenant_context_is_denied(self):
        request = self.factory.get("/roles/")
        force_authenticate(request, user=self.user)
        request.tenant = None
        response = self.view(request)
        self.assertEqual(response.status_code, 403)


class HasTenantPermissionViewSetTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.tenant = Tenant.objects.create(name="A", slug="a")
        self.view = _ManageMembersViewSet.as_view({"get": "list"})

    def _get(self, user, tenant):
        request = self.factory.get("/members/")
        force_authenticate(request, user=user)
        request.tenant = tenant
        return self.view(request)

    def test_non_member_denied(self):
        user = User.objects.create_user(username="out", password="x")
        self.assertEqual(self._get(user, self.tenant).status_code, 403)

    def test_member_without_permission_denied(self):
        user = User.objects.create_user(username="m", password="x")
        _add_member(user, self.tenant, "member")
        self.assertEqual(self._get(user, self.tenant).status_code, 403)

    def test_admin_with_permission_allowed(self):
        user = User.objects.create_user(username="a", password="x")
        _add_member(user, self.tenant, "admin")
        self.assertEqual(self._get(user, self.tenant).status_code, 200)

    def test_super_admin_allowed_without_membership(self):
        user = User.objects.create_user(
            username="root", password="x", is_super_admin=True
        )
        self.assertEqual(self._get(user, self.tenant).status_code, 200)
