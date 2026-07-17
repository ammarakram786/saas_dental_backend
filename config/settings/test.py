"""Test settings: self-contained, no external Postgres/Redis required."""
import os

# Ensure required secrets exist before base settings are imported.
os.environ.setdefault("DJANGO_SECRET_KEY", "ci-test-secret-key-not-for-production")
os.environ.setdefault(
    "FIELD_ENCRYPTION_KEY",
    "MDEyMzQ1Njc4OTAxMjM0NTY3ODkwMTIzNDU2Nzg5MDE=",  # base64 of 32 ASCII bytes
)

from .base import *  # noqa: F403, E402

DEBUG = False
ALLOWED_HOSTS = ["*"]
ENABLE_API_DOCS = True

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

# Avoid Celery broker during unit tests.
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True
