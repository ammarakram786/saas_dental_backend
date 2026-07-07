from django.db import models

from apps.common.models import TimeStampedModel


class PlatformUserProfile(TimeStampedModel):
    user = models.OneToOneField(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="platform_profile",
    )
    contact_phone = models.CharField(max_length=30, blank=True)
    avatar = models.ImageField(upload_to="avatars/platform/", blank=True, null=True)

    def __str__(self) -> str:
        return f"PlatformProfile<{self.user_id}>"
