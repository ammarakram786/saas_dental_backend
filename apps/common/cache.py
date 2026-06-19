"""Caching helpers for RBAC and tenant resolution.

All entries live in the dedicated ``permissions`` cache (see CACHES in settings)
so they can be reasoned about and flushed independently of the default cache.
"""
from __future__ import annotations

from django.core.cache import caches

PERMISSIONS_CACHE_ALIAS = "permissions"
DEFAULT_TIMEOUT = 300  # seconds

_PLATFORM_ROLE_MODULES_KEY = "rbac:platform_role:{role_id}:modules"
_TENANT_ROLE_PERMS_KEY = "rbac:tenant_role:{role_id}:perms"
_TENANT_BY_SLUG_KEY = "tenant:slug:{slug}"
_TENANT_BY_ID_KEY = "tenant:id:{tenant_id}"


def _cache():
    return caches[PERMISSIONS_CACHE_ALIAS]


def get_platform_role_modules(role) -> frozenset[str]:
    """Return cached active module codenames for a ``PlatformRole``."""
    key = _PLATFORM_ROLE_MODULES_KEY.format(role_id=role.pk)
    cached = _cache().get(key)
    if cached is None:
        cached = list(role.module_codenames())
        _cache().set(key, cached, DEFAULT_TIMEOUT)
    return frozenset(cached)


def invalidate_platform_role(role_id) -> None:
    _cache().delete(_PLATFORM_ROLE_MODULES_KEY.format(role_id=role_id))


def get_tenant_role_permissions(role) -> frozenset[str]:
    """Return cached active permission codenames for a ``TenantRole``."""
    key = _TENANT_ROLE_PERMS_KEY.format(role_id=role.pk)
    cached = _cache().get(key)
    if cached is None:
        cached = list(role.permission_codenames())
        _cache().set(key, cached, DEFAULT_TIMEOUT)
    return frozenset(cached)


def invalidate_tenant_role(role_id) -> None:
    _cache().delete(_TENANT_ROLE_PERMS_KEY.format(role_id=role_id))


def cache_tenant(tenant) -> None:
    _cache().set(_TENANT_BY_SLUG_KEY.format(slug=tenant.slug), tenant, DEFAULT_TIMEOUT)
    _cache().set(_TENANT_BY_ID_KEY.format(tenant_id=tenant.pk), tenant, DEFAULT_TIMEOUT)


def get_cached_tenant_by_slug(slug):
    return _cache().get(_TENANT_BY_SLUG_KEY.format(slug=slug))


def get_cached_tenant_by_id(tenant_id):
    return _cache().get(_TENANT_BY_ID_KEY.format(tenant_id=tenant_id))


def invalidate_tenant(*, slug=None, tenant_id=None) -> None:
    if slug is not None:
        _cache().delete(_TENANT_BY_SLUG_KEY.format(slug=slug))
    if tenant_id is not None:
        _cache().delete(_TENANT_BY_ID_KEY.format(tenant_id=tenant_id))
