from django.db import models

from apps.common.models import TimeStampedModel


class TenantUserProfile(TimeStampedModel):
    user = models.OneToOneField(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="tenant_profile",
    )
    tenant = models.ForeignKey(
        "tenants.Tenant",
        on_delete=models.CASCADE,
        related_name="user_profiles",
    )
    job_title = models.CharField(max_length=120, blank=True)
    specialization = models.CharField(max_length=120, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("user", "tenant"),
                name="uniq_tenant_user_profile_per_tenant",
            )
        ]

    def __str__(self) -> str:
        return f"TenantProfile<{self.user_id}@{self.tenant_id}>"
