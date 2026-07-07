from django.db import models

from apps.common.models import TimeStampedModel
from apps.tenants.models import TenantResource


class AppointmentSlot(TimeStampedModel, TenantResource):
    dentist = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="appointment_slots",
    )
    chair = models.ForeignKey(
        "appointments.ClinicAsset",
        on_delete=models.PROTECT,
        related_name="slots",
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_available = models.BooleanField(default=True)

    class Meta:
        ordering = ("start_time",)

    def __str__(self) -> str:
        return f"Slot<{self.tenant_id}:{self.start_time.isoformat()}>"
