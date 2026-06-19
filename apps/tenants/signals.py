from django.db.models.signals import (
    m2m_changed,
    post_delete,
    post_save,
)
from django.dispatch import receiver

from apps.common.cache import (
    cache_tenant,
    invalidate_tenant,
    invalidate_tenant_role,
)
from apps.tenants.models import Tenant, TenantRole


@receiver(post_save, sender=Tenant)
def _seed_roles_and_cache_tenant(sender, instance, created, **kwargs):
    # Import here to avoid an import cycle at app-loading time.
    from apps.tenants.services import seed_default_roles

    if created:
        seed_default_roles(instance)

    # Only active tenants are resolvable, so never cache an inactive one;
    # proactively evict if a tenant was just deactivated.
    if instance.is_active:
        cache_tenant(instance)
    else:
        invalidate_tenant(slug=instance.slug, tenant_id=instance.pk)


@receiver(post_delete, sender=Tenant)
def _invalidate_tenant_cache(sender, instance, **kwargs):
    invalidate_tenant(slug=instance.slug, tenant_id=instance.pk)


@receiver([post_save, post_delete], sender=TenantRole)
def _invalidate_tenant_role(sender, instance, **kwargs):
    invalidate_tenant_role(instance.pk)


@receiver(m2m_changed, sender=TenantRole.permissions.through)
def _invalidate_tenant_role_on_perms_change(sender, instance, **kwargs):
    invalidate_tenant_role(instance.pk)
