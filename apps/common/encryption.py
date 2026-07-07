from __future__ import annotations

import base64
import os

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from django.conf import settings


def _aesgcm() -> AESGCM:
    return AESGCM(settings.FIELD_ENCRYPTION_KEY_BYTES)


def encrypt_text(value: str | None) -> str:
    if not value:
        return ""

    nonce = os.urandom(12)
    ciphertext = _aesgcm().encrypt(nonce, value.encode("utf-8"), None)
    return base64.b64encode(nonce + ciphertext).decode("ascii")


def decrypt_text(value: str | None) -> str:
    if not value:
        return ""

    raw = base64.b64decode(value)
    nonce, ciphertext = raw[:12], raw[12:]
    return _aesgcm().decrypt(nonce, ciphertext, None).decode("utf-8")
