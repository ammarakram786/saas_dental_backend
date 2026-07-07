from django.db import models

from apps.common.models import TimeStampedModel


class PlatformAuditEvent(TimeStampedModel):
    SEVERITY_CHOICES = [
        ("info", "Info"),
        ("warning", "Warning"),
        ("critical", "Critical"),
    ]

    actor = models.CharField(max_length=150)
    action = models.CharField(max_length=255)
    target = models.CharField(max_length=255, blank=True)
    severity = models.CharField(max_length=16, choices=SEVERITY_CHOICES, default="info")
    category = models.CharField(max_length=64, blank=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return f"{self.actor}: {self.action}"
