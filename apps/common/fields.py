from __future__ import annotations

from django.db import models

from apps.common.encryption import decrypt_text, encrypt_text


class EncryptedTextField(models.TextField):
    """Simple AES-GCM encrypted text field for low-volume sensitive values."""

    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        return encrypt_text(value)

    def from_db_value(self, value, expression, connection):
        return decrypt_text(value)

    def to_python(self, value):
        value = super().to_python(value)
        if value in (None, ""):
            return value
        try:
            return decrypt_text(value)
        except Exception:
            return value
