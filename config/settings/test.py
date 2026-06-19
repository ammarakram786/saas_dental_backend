"""Test settings: self-contained, no external Postgres/Redis required."""
from .base import *  # noqa: F403

DEBUG = False
ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "default",
    },
    "permissions": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "permissions",
    },
}

PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
