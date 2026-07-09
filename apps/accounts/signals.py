import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.accounts.models import PlatformUserProfile, User

logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def user_post_save_hook(sender, instance, created, **kwargs):
    logger.debug(
        "user_post_save_hook: user_id=%s created=%s",
        instance.pk,
        created,
    )

    if instance.is_superuser:
        PlatformUserProfile.objects.update_or_create(
            user=instance,
            defaults={"is_super_admin": True},
        )
        return

    profile = PlatformUserProfile.objects.filter(user=instance).first()
    if profile is not None and profile.is_super_admin:
        profile.is_super_admin = False
        profile.save(update_fields=["is_super_admin", "updated_at"])
