"""Tenant resolution middleware.

Resolves the active tenant from the ``X-Tenant-ID`` header (slug or numeric id)
or, failing that, the request subdomain, and attaches it to ``request.tenant``
(``None`` when unresolved). Enforcement is delegated to permissions/viewsets so
that public and platform endpoints keep working without a tenant context.

Implements the sync/async dual interface so it runs natively under Django 6's
ASGI stack without forcing a sync context.
"""
from __future__ import annotations

from asgiref.sync import iscoroutinefunction, markcoroutinefunction, sync_to_async

# Hosts that never carry a tenant subdomain.
_BARE_HOSTS = {"localhost", "127.0.0.1", "0.0.0.0"}
_IGNORED_SUBDOMAINS = {"www", "api", "admin"}


class TenantResolutionMiddleware:
    async_capable = True
    sync_capable = True

    def __init__(self, get_response):
        self.get_response = get_response
        self._is_async = iscoroutinefunction(get_response)
        if self._is_async:
            markcoroutinefunction(self)

    def __call__(self, request):
        if self._is_async:
            return self.__acall__(request)
        request.tenant = self._resolve(request)
        return self.get_response(request)

    async def __acall__(self, request):
        request.tenant = await sync_to_async(self._resolve)(request)
        return await self.get_response(request)

    def _resolve(self, request):
        identifier = request.headers.get("X-Tenant-ID")
        if identifier:
            return self._lookup(identifier.strip())

        subdomain = self._extract_subdomain(request)
        if subdomain:
            return self._lookup_by_slug(subdomain)
        return None

    @staticmethod
    def _extract_subdomain(request) -> str | None:
        host = request.get_host().split(":", 1)[0].lower()
        if host in _BARE_HOSTS:
            return None
        labels = host.split(".")
        if len(labels) < 3:
            return None
        subdomain = labels[0]
        if subdomain in _IGNORED_SUBDOMAINS:
            return None
        return subdomain

    def _lookup(self, identifier: str):
        if identifier.isdigit():
            return self._lookup_by_id(int(identifier))
        return self._lookup_by_slug(identifier)

    @staticmethod
    def _lookup_by_slug(slug: str):
        from apps.common.cache import cache_tenant, get_cached_tenant_by_slug
        from apps.tenants.models import Tenant

        cached = get_cached_tenant_by_slug(slug)
        if cached is not None:
            return cached
        tenant = Tenant.objects.filter(slug=slug, is_active=True).first()
        if tenant is not None:
            cache_tenant(tenant)
        return tenant

    @staticmethod
    def _lookup_by_id(tenant_id: int):
        from apps.common.cache import cache_tenant, get_cached_tenant_by_id
        from apps.tenants.models import Tenant

        cached = get_cached_tenant_by_id(tenant_id)
        if cached is not None:
            return cached
        tenant = Tenant.objects.filter(pk=tenant_id, is_active=True).first()
        if tenant is not None:
            cache_tenant(tenant)
        return tenant
