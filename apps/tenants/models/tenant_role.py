from django.db import models

from apps.common.models import TimeStampedModel
from apps.tenants.models.tenant_resource import TenantResource


class TenantRole(TimeStampedModel, TenantResource):
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150)
    description = models.TextField(blank=True)
    is_system = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    permissions = models.ManyToManyField(
        "tenants.TenantPermission",
        related_name="roles",
        blank=True,
    )

    class Meta:
        ordering = ("name",)
        verbose_name = "Tenant Role"
        verbose_name_plural = "Tenant Roles"
        constraints = [
            models.UniqueConstraint(
                fields=("tenant", "slug"),
                name="uniq_tenant_role_slug_per_tenant",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.tenant.slug}:{self.slug}"

    def permission_codenames(self) -> set[str]:
        return set(
            self.permissions.filter(is_active=True).values_list("codename", flat=True)
        )
