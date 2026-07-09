from django.db import models

from apps import appointments, accounts
from apps.common.fields import EncryptedTextField
from apps.common.models import TimeStampedModel
from apps.tenants.models import TenantResource


class ClinicalNote(TimeStampedModel, TenantResource):
    appointment = models.ForeignKey(
        "appointments.Appointment",
        on_delete=models.CASCADE,
        related_name="clinical_notes",
    )
    dentist = models.ForeignKey(
        "accounts.User",
        on_delete=models.PROTECT,
        related_name="clinical_notes",
    )
    body = EncryptedTextField()
    is_locked = models.BooleanField(default=False)
    locked_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return f"ClinicalNote<{self.pk}>"
