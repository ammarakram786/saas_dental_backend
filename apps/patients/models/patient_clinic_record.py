from django.db import models

from apps.common.fields import EncryptedTextField
from apps.common.models import TimeStampedModel


class PatientClinicRecord(TimeStampedModel):
    patient = models.ForeignKey(
        "accounts.PatientUserProfile",
        on_delete=models.CASCADE,
        related_name="clinic_records",
    )
    tenant = models.ForeignKey(
        "tenants.Tenant",
        on_delete=models.CASCADE,
        related_name="patient_records",
    )
    allergy_overrides = EncryptedTextField(blank=True)
    consent_given = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("patient", "tenant"),
                name="uniq_patient_clinic_record",
            )
        ]

    def __str__(self) -> str:
        return f"PatientClinicRecord<{self.patient_id}@{self.tenant_id}>"
