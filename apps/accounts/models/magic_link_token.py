import uuid

from django.db import models
from django.utils import timezone

from apps.common.models import TimeStampedModel


class MagicLinkToken(TimeStampedModel):
    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="magic_link_tokens",
    )
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    expires_at = models.DateTimeField()
    consumed_at = models.DateTimeField(blank=True, null=True)

    @property
    def is_valid(self) -> bool:
        return self.consumed_at is None and timezone.now() < self.expires_at

    def mark_consumed(self) -> None:
        self.consumed_at = timezone.now()
        self.save(update_fields=["consumed_at"])

    def __str__(self) -> str:
        return f"MagicLinkToken<{self.user_id}:{self.token}>"
