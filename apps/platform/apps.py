from django.apps import AppConfig


class PlatformConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.platform"
    label = "platform"
    verbose_name = "Platform Control Plane"

    def ready(self):
        import apps.platform.signals  # noqa: F401
