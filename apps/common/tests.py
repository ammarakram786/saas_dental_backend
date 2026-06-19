from django.core.cache import caches
from django.test import RequestFactory, TestCase

from apps.common.middleware import TenantResolutionMiddleware
from apps.tenants.models import Tenant


def _passthrough(request):
    return "RESPONSE"


class TenantResolutionMiddlewareTests(TestCase):
    def setUp(self):
        caches["permissions"].clear()
        self.factory = RequestFactory()
        self.middleware = TenantResolutionMiddleware(_passthrough)
        self.tenant = Tenant.objects.create(name="Acme", slug="acme")

    def _run(self, **extra):
        request = self.factory.get("/", **extra)
        self.middleware(request)
        return request

    def test_resolves_from_header_slug(self):
        request = self._run(HTTP_X_TENANT_ID="acme")
        self.assertEqual(request.tenant, self.tenant)

    def test_resolves_from_header_numeric_id(self):
        request = self._run(HTTP_X_TENANT_ID=str(self.tenant.pk))
        self.assertEqual(request.tenant, self.tenant)

    def test_resolves_from_subdomain(self):
        request = self._run(HTTP_HOST="acme.example.com")
        self.assertEqual(request.tenant, self.tenant)

    def test_ignored_subdomain_resolves_to_none(self):
        request = self._run(HTTP_HOST="www.example.com")
        self.assertIsNone(request.tenant)

    def test_bare_host_resolves_to_none(self):
        request = self._run(HTTP_HOST="localhost")
        self.assertIsNone(request.tenant)

    def test_unknown_tenant_resolves_to_none(self):
        request = self._run(HTTP_X_TENANT_ID="ghost")
        self.assertIsNone(request.tenant)

    def test_inactive_tenant_is_not_resolved(self):
        Tenant.objects.create(name="Dormant", slug="dormant", is_active=False)
        request = self._run(HTTP_X_TENANT_ID="dormant")
        self.assertIsNone(request.tenant)
