from __future__ import annotations

import base64
import os

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.utils import timezone

from apps.accounts.models import WebAuthnCredential

User = get_user_model()

CHALLENGE_TTL_SECONDS = 300


def _challenge_key(purpose: str, identifier: str) -> str:
    return f"webauthn:{purpose}:{identifier}"


def generate_challenge() -> str:
    return base64.urlsafe_b64encode(os.urandom(32)).rstrip(b"=").decode("ascii")


def begin_registration(*, identifier: str, display_name: str, username: str) -> dict:
    challenge = generate_challenge()
    cache.set(
        _challenge_key("register", identifier),
        {
            "challenge": challenge,
            "display_name": display_name,
            "username": username,
            "created_at": timezone.now().isoformat(),
        },
        CHALLENGE_TTL_SECONDS,
    )
    return {
        "challenge": challenge,
        "rp": {"name": "Dental Doodle", "id": "localhost"},
        "user": {
            "id": identifier,
            "name": username,
            "displayName": display_name or username,
        },
        "timeout": CHALLENGE_TTL_SECONDS * 1000,
    }


def finish_registration(*, user, credential: dict, device_name: str = "") -> WebAuthnCredential:
    raw_id = credential.get("id") or credential.get("rawId") or ""
    public_key = credential.get("publicKey") or credential.get("response", {}).get(
        "publicKey",
        "",
    )
    sign_count = credential.get("signCount", 0)
    transports = credential.get("response", {}).get("transports", [])
    return WebAuthnCredential.objects.create(
        user=user,
        credential_id=raw_id,
        public_key=public_key,
        sign_count=sign_count or 0,
        device_name=device_name,
        transports=transports,
    )


def begin_authentication(*, identifier: str) -> dict:
    challenge = generate_challenge()
    cache.set(_challenge_key("authenticate", identifier), challenge, CHALLENGE_TTL_SECONDS)

    credentials = WebAuthnCredential.objects.filter(user__username=identifier, is_active=True)
    return {
        "challenge": challenge,
        "allowCredentials": [
            {
                "id": credential.credential_id,
                "type": "public-key",
                "transports": credential.transports,
            }
            for credential in credentials
        ],
        "timeout": CHALLENGE_TTL_SECONDS * 1000,
    }


def finish_authentication(*, identifier: str, credential: dict):
    raw_id = credential.get("id") or credential.get("rawId") or ""
    user = User.objects.filter(username=identifier).first()
    if user is None:
        return None

    device = next(
        (
            item
            for item in user.webauthn_credentials.filter(is_active=True)
            if item.credential_id == raw_id
        ),
        None,
    )
    if device is None:
        return None

    device.sign_count += 1
    device.save(update_fields=["sign_count", "updated_at"])
    return user
