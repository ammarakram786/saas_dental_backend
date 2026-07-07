from django.db import models

from apps.common.models import TimeStampedModel
from apps.tenants.models import TenantResource


class Odontogram(TimeStampedModel, TenantResource):
    appointment = models.OneToOneField(
        "appointments.Appointment",
        on_delete=models.CASCADE,
        related_name="odontogram",
    )
    tooth_map = models.JSONField(default=dict, blank=True)

    def __str__(self) -> str:
        return f"Odontogram<{self.appointment_id}>"
