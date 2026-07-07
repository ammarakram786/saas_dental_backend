from django.db import models

from apps.common.models import TimeStampedModel
from apps.tenants.models import TenantResource


class Prescription(TimeStampedModel, TenantResource):
    clinical_note = models.ForeignKey(
        "clinical.ClinicalNote",
        on_delete=models.CASCADE,
        related_name="prescriptions",
    )
    medications = models.JSONField(default=list, blank=True)

    def __str__(self) -> str:
        return f"Prescription<{self.pk}>"
