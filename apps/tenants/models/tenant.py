from django.db import models

from apps.common.models import TimeStampedModel


class Tenant(TimeStampedModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(
        max_length=100,
        unique=True,
        db_index=True,
        help_text="Subdomain / X-Tenant-ID key used to resolve the tenant.",
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ("name",)
        verbose_name = "Tenant"
        verbose_name_plural = "Tenants"

    def __str__(self) -> str:
        return self.name
