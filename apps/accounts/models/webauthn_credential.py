from django.db import models

from apps.common.fields import EncryptedTextField
from apps.common.models import TimeStampedModel


class WebAuthnCredential(TimeStampedModel):
    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="webauthn_credentials",
    )
    credential_id = EncryptedTextField()
    public_key = EncryptedTextField()
    sign_count = models.PositiveBigIntegerField(default=0)
    device_name = models.CharField(max_length=120, blank=True)
    transports = models.JSONField(default=list, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"WebAuthnCredential<{self.user_id}:{self.device_name or 'device'}>"
