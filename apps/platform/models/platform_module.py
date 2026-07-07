from django.db import models

from apps.common.models import TimeStampedModel


class PlatformModule(TimeStampedModel):
    codename = models.SlugField(
        max_length=100,
        unique=True,
        help_text="Stable machine identifier, e.g. 'manage_billing'.",
    )
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ("codename",)
        verbose_name = "Platform Module"
        verbose_name_plural = "Platform Modules"

    def __str__(self) -> str:
        return self.codename
