from django.db import models

from apps.common.models import TimeStampedModel
from apps.tenants.models import TenantResource


class PaymentRecord(TimeStampedModel, TenantResource):
    METHOD_CHOICES = [
        ("cash", "Cash"),
        ("jazzcash", "JazzCash"),
    ]
    GATEWAY_STATUS_CHOICES = [
        ("pending", "Pending"),
        ("success", "Success"),
        ("failed", "Failed"),
        ("manual", "Manual"),
    ]

    invoice = models.ForeignKey(
        "billing.Invoice",
        on_delete=models.CASCADE,
        related_name="payments",
    )
    method = models.CharField(max_length=12, choices=METHOD_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    gateway_ref = models.CharField(max_length=120, blank=True)
    gateway_status = models.CharField(
        max_length=12,
        choices=GATEWAY_STATUS_CHOICES,
        default="pending",
    )

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return f"Payment<{self.pk}:{self.method}:{self.gateway_status}>"
