from django.db import models

from apps import accounts, appointments
from apps.common.models import TimeStampedModel
from apps.tenants.models import TenantResource


class Appointment(TimeStampedModel, TenantResource):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("arrived", "Arrived"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    patient = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="patient_appointments",
    )
    slot = models.ForeignKey(
        "appointments.AppointmentSlot",
        on_delete=models.PROTECT,
        related_name="appointments",
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    appointment_type = models.CharField(max_length=120)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return f"Appointment<{self.pk}:{self.status}>"
