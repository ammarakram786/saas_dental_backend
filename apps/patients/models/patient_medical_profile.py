from django.db import models

from apps.common.fields import EncryptedTextField
from apps.common.models import TimeStampedModel


class PatientMedicalProfile(TimeStampedModel):
    patient = models.OneToOneField(
        "accounts.PatientUserProfile",
        on_delete=models.CASCADE,
        related_name="medical_profile",
    )
    global_health_notes = EncryptedTextField(blank=True)

    def __str__(self) -> str:
        return f"PatientMedicalProfile<{self.patient_id}>"
