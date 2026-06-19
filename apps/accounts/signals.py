import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.accounts.models import User

logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def user_post_save_hook(sender, instance, created, **kwargs):
    logger.debug(
        "user_post_save_hook: user_id=%s created=%s",
        instance.pk,
        created,
    )
