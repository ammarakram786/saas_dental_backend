from django.core.exceptions import ValidationError
from django.db import models

from apps.common.models import TimeStampedModel


class TenantMembership(TimeStampedModel):
    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="tenant_memberships",
    )
    tenant = models.ForeignKey(
        "tenants.Tenant",
        on_delete=models.CASCADE,
        related_name="memberships",
    )
    role = models.ForeignKey(
        "tenants.TenantRole",
        on_delete=models.PROTECT,
        related_name="memberships",
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Tenant Membership"
        verbose_name_plural = "Tenant Memberships"
        constraints = [
            models.UniqueConstraint(
                fields=("user", "tenant"),
                name="uniq_user_per_tenant",
            ),
        ]
        indexes = [models.Index(fields=("tenant", "user"))]

    def __str__(self) -> str:
        return f"{self.user} @ {self.tenant.slug} ({self.role.slug})"

    def clean(self):
        super().clean()
        if self.role_id and self.tenant_id and self.role.tenant_id != self.tenant_id:
            raise ValidationError(
                {"role": "Role must belong to the same tenant as the membership."}
            )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
