from django.db.models.signals import m2m_changed, post_delete, post_save
from django.dispatch import receiver

from apps.common.cache import invalidate_platform_role
from apps.platform.models import PlatformModule, PlatformRole


@receiver([post_save, post_delete], sender=PlatformRole)
def _invalidate_role_on_change(sender, instance, **kwargs):
    invalidate_platform_role(instance.pk)


@receiver(m2m_changed, sender=PlatformRole.modules.through)
def _invalidate_role_on_modules_change(sender, instance, **kwargs):
    invalidate_platform_role(instance.pk)


@receiver([post_save, post_delete], sender=PlatformModule)
def _invalidate_roles_on_module_change(sender, instance, **kwargs):
    # A module toggled active/inactive (or renamed) affects every role using it.
    for role_id in instance.roles.values_list("pk", flat=True):
        invalidate_platform_role(role_id)
