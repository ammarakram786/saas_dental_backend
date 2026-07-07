from django.db import models

from apps.common.models import TimeStampedModel
from apps.tenants.models import TenantResource


class TreatmentPlan(TimeStampedModel, TenantResource):
    appointment = models.ForeignKey(
        "appointments.Appointment",
        on_delete=models.CASCADE,
        related_name="treatment_plans",
    )
    phases = models.JSONField(default=list, blank=True)
    estimated_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    consent_signed = models.BooleanField(default=False)
    consent_signed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return f"TreatmentPlan<{self.pk}>"
