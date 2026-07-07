from django.db import models

from apps.common.models import TimeStampedModel
from apps.tenants.models import TenantResource


class Invoice(TimeStampedModel, TenantResource):
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("issued", "Issued"),
        ("paid", "Paid"),
        ("void", "Void"),
    ]

    appointment = models.ForeignKey(
        "appointments.Appointment",
        on_delete=models.CASCADE,
        related_name="invoices",
    )
    patient = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="patient_invoices",
    )
    line_items = models.JSONField(default=list, blank=True)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    insurance_coverage = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    copay_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default="draft")

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return f"Invoice<{self.pk}:{self.status}>"
