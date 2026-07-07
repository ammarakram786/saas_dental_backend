from django.db import models

from apps.common.models import TimeStampedModel


class TenantPermission(TimeStampedModel):
    codename = models.SlugField(max_length=100, unique=True)
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ("codename",)
        verbose_name = "Tenant Permission"
        verbose_name_plural = "Tenant Permissions"

    def __str__(self) -> str:
        return self.codename
