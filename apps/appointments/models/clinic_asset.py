from django.db import models

from apps.common.models import TimeStampedModel
from apps.tenants.models import TenantResource


class ClinicAsset(TimeStampedModel, TenantResource):
    ASSET_TYPE_CHOICES = [
        ("chair", "Chair"),
        ("xray", "X-Ray"),
        ("suite", "Suite"),
    ]

    name = models.CharField(max_length=120)
    asset_type = models.CharField(max_length=32, choices=ASSET_TYPE_CHOICES)
    is_operational = models.BooleanField(default=True)

    class Meta:
        ordering = ("name",)

    def __str__(self) -> str:
        return f"{self.tenant_id}:{self.name}"
