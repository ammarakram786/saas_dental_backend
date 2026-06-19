"""Local development settings."""
from .base import *  # noqa: F403

DEBUG = True
ENABLE_TLS_HARDENING = False

# Relax for runserver; production enables TLS hardening via env.
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
