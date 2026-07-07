from django.db import models


class TenantResource(models.Model):
    tenant = models.ForeignKey(
        "tenants.Tenant",
        on_delete=models.CASCADE,
        db_index=True,
        related_name="+",
    )

    class Meta:
        abstract = True
