from django.db import models

from apps.common.models import TimeStampedModel
from apps.tenants.models import TenantResource


class InsurancePanel(TimeStampedModel, TenantResource):
    insurer_name = models.CharField(max_length=150)
    panel_code = models.CharField(max_length=100)
    coverage_rules = models.JSONField(default=dict, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("tenant", "panel_code"),
                name="uniq_insurance_panel_code_per_tenant",
            )
        ]

    def __str__(self) -> str:
        return f"{self.insurer_name} ({self.panel_code})"
