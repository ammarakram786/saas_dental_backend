# Dental SaaS — Backend

Django REST API for the dental clinic management platform (multi-tenant clinics, appointments, clinical notes, billing, platform admin).

## Requirements

- Python 3.13+
- PostgreSQL
- Redis (cache, permissions cache, Celery broker)

## Quick start

```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env        # or create .env from the example below
# edit .env — set DJANGO_SECRET_KEY, FIELD_ENCRYPTION_KEY, DATABASE_URL

python manage.py migrate
python manage.py seed_permissions
python manage.py seed_platform_modules
# optional demo data (password for all demo users: DemoPass123!)
python manage.py create_demo_clinic

python manage.py runserver 127.0.0.1:5000
# or
gunicorn config.wsgi:application --bind 127.0.0.1:5000 --reload
```

Celery (optional, for scheduled jobs):

```bash
celery -A config worker -l info
celery -A config beat -l info
```

API docs (when `ENABLE_API_DOCS=True` or `DJANGO_DEBUG=True`): `/api/schema/swagger-ui/`

## Environment

Django loads `backend/.env` via `django-environ` (`config/settings/base.py`).

Generate secrets:

```bash
# Django secret
python3 -c "import secrets; print(secrets.token_urlsafe(50))"

# AES-256 field encryption key (exactly 32 bytes, base64)
python3 -c "import os, base64; print(base64.b64encode(os.urandom(32)).decode())"
```

### Local — `.env`

```env
DJANGO_SETTINGS_MODULE=config.settings.local
DJANGO_SECRET_KEY=replace-with-token-urlsafe-50
DJANGO_DEBUG=True
ENABLE_TLS_HARDENING=False
ENABLE_API_DOCS=True

ALLOWED_HOSTS=localhost,127.0.0.1

DATABASE_URL=postgres://postgres:postgres@127.0.0.1:5432/dental_saas

REDIS_URL=redis://127.0.0.1:6379/0
REDIS_PERMISSIONS_URL=redis://127.0.0.1:6379/1
CELERY_BROKER_URL=redis://127.0.0.1:6379/0
CELERY_RESULT_BACKEND=redis://127.0.0.1:6379/0

# Must be base64 of exactly 32 bytes
FIELD_ENCRYPTION_KEY=replace-with-base64-of-32-random-bytes=

# Optional; defaults to DJANGO_SECRET_KEY
# JWT_SIGNING_KEY=
```

### Production — `.env.production`

Use with systemd `EnvironmentFile=` or copy to `.env` on the server. Point settings at production:

```env
DJANGO_SETTINGS_MODULE=config.settings.production
DJANGO_SECRET_KEY=replace-with-strong-unique-secret
DJANGO_DEBUG=False
ENABLE_TLS_HARDENING=True
ENABLE_API_DOCS=False

ALLOWED_HOSTS=your.domain.example,127.0.0.1

DATABASE_URL=postgres://USER:PASSWORD@HOST:5432/dental_saas

REDIS_URL=redis://127.0.0.1:6379/0
REDIS_PERMISSIONS_URL=redis://127.0.0.1:6379/1
CELERY_BROKER_URL=redis://127.0.0.1:6379/0
CELERY_RESULT_BACKEND=redis://127.0.0.1:6379/0

FIELD_ENCRYPTION_KEY=replace-with-base64-of-32-random-bytes=

# JWT_SIGNING_KEY=
```

### Variable reference

| Variable | Required | Notes |
|----------|----------|--------|
| `DJANGO_SECRET_KEY` | yes | Django signing / crypto |
| `DJANGO_DEBUG` | yes | `True` only for local |
| `FIELD_ENCRYPTION_KEY` | yes | Base64 of **exactly 32 bytes**; changing it makes existing encrypted fields unreadable |
| `DATABASE_URL` | yes | `postgres://user:pass@host:5432/dbname` |
| `ALLOWED_HOSTS` | no | Comma-separated; defaults to `localhost,127.0.0.1` |
| `REDIS_URL` | no | Default `redis://127.0.0.1:6379/0` |
| `REDIS_PERMISSIONS_URL` | no | Default DB `1` on local Redis |
| `CELERY_BROKER_URL` / `CELERY_RESULT_BACKEND` | no | Default to `REDIS_URL` |
| `ENABLE_TLS_HARDENING` | no | Production HSTS / secure cookies (also forced in `config.settings.production`) |
| `ENABLE_API_DOCS` | no | OpenAPI / Swagger UI |
| `JWT_SIGNING_KEY` | no | Defaults to `DJANGO_SECRET_KEY` |
| `DJANGO_SETTINGS_MODULE` | recommended | `config.settings.local` or `config.settings.production` |

## Useful management commands

```bash
python manage.py seed_permissions
python manage.py seed_platform_modules
python manage.py create_demo_clinic   # demo users password: DemoPass123!
python manage.py migrate
python manage.py collectstatic --noinput
```

## Docker

```bash
docker build -t dental-saas-backend .
docker run --env-file .env -p 5000:5000 dental-saas-backend
```

Image migrates, collects static, and runs gunicorn on `0.0.0.0:5000`.

## Layout

- `config/` — Django settings, URLs, WSGI/ASGI, Celery
- `apps/` — domain apps (`accounts`, `tenants`, `appointments`, `patients`, `clinical`, `billing`, `platform`, …)
