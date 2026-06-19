from django.core.exceptions import ValidationError
from django.db import models

from apps.common.models import TimeStampedModel


class Tenant(TimeStampedModel):
    """A customer organization. The unit of data isolation."""

    name = models.CharField(max_length=255)
    slug = models.SlugField(
        max_length=100,
        unique=True,
        db_index=True,
        help_text="Subdomain / X-Tenant-ID key used to resolve the tenant.",
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ("name",)
        verbose_name = "Tenant"
        verbose_name_plural = "Tenants"

    def __str__(self) -> str:
        return self.name


class TenantResource(TimeStampedModel):
    """Abstract base for every tenant-owned model.

    Inheriting this guarantees a ``tenant`` foreign key exists so that
    ``BaseTenantViewSet`` and isolation queries can filter consistently.
    """

    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        db_index=True,
        related_name="+",
    )

    class Meta:
        abstract = True


class TenantPermission(TimeStampedModel):
    """Global catalog of data-plane permission codenames.

    These are the fixed vocabulary a tenant composes its dynamic roles from
    (e.g. ``manage_members``, ``manage_appointments``, ``view_reports``).
    """

    codename = models.SlugField(max_length=100, unique=True)
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ("codename",)
        verbose_name = "Tenant Permission"
        verbose_name_plural = "Tenant Permissions"

    def __str__(self) -> str:
        return self.codename


class TenantRole(TenantResource):
    """A dynamic, per-tenant role composed of tenant permissions.

    Each tenant owns and customizes its own roles; ``is_system`` marks the
    defaults seeded on tenant creation so they can be protected from deletion.
    """

    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150)
    description = models.TextField(blank=True)
    is_system = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    permissions = models.ManyToManyField(
        TenantPermission,
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


class TenantMembership(TimeStampedModel):
    """Through-table mapping a user to a tenant with a dynamic role."""

    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="tenant_memberships",
    )
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name="memberships",
    )
    role = models.ForeignKey(
        TenantRole,
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
        indexes = [
            models.Index(fields=("tenant", "user")),
        ]

    def __str__(self) -> str:
        return f"{self.user} @ {self.tenant.slug} ({self.role.slug})"

    def clean(self):
        super().clean()
        if self.role_id and self.tenant_id and self.role.tenant_id != self.tenant_id:
            raise ValidationError(
                {"role": "Role must belong to the same tenant as the membership."}
            )

    def save(self, *args, **kwargs):
        # Enforce cross-tenant role integrity even outside ModelForm validation.
        self.clean()
        super().save(*args, **kwargs)
