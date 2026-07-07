from django.db import models

from apps.common.fields import EncryptedTextField
from apps.common.models import TimeStampedModel


class PatientUserProfile(TimeStampedModel):
    BLOOD_GROUP_CHOICES = [
        ("A+", "A+"),
        ("A-", "A-"),
        ("B+", "B+"),
        ("B-", "B-"),
        ("AB+", "AB+"),
        ("AB-", "AB-"),
        ("O+", "O+"),
        ("O-", "O-"),
        ("UNK", "Unknown"),
    ]

    user = models.OneToOneField(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="patient_profile",
    )
    date_of_birth = models.DateField(blank=True, null=True)
    cnic = models.CharField(max_length=15, blank=True)
    primary_phone = models.CharField(max_length=30, blank=True)
    blood_type = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES, default="UNK")
    systemic_conditions = EncryptedTextField(blank=True)
    allergies = EncryptedTextField(blank=True)
    active_medications = EncryptedTextField(blank=True)

    def __str__(self) -> str:
        return f"PatientProfile<{self.user_id}>"
