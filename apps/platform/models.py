from django.db import models

from apps.common.models import TimeStampedModel


class PlatformModule(TimeStampedModel):
    """A unit of control-plane functionality (e.g. ``manage_billing``).

    Modules form the vocabulary that platform roles are composed from and that
    platform endpoints gate against via ``required_module_codename``.
    """

    codename = models.SlugField(
        max_length=100,
        unique=True,
        help_text="Stable machine identifier, e.g. 'manage_billing'.",
    )
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ("codename",)
        verbose_name = "Platform Module"
        verbose_name_plural = "Platform Modules"

    def __str__(self) -> str:
        return self.codename


class PlatformRole(TimeStampedModel):
    """A named bundle of platform modules assignable to a user.

    Roles are database-driven so the control-plane permission matrix can evolve
    without code changes.
    """

    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=150, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    modules = models.ManyToManyField(
        PlatformModule,
        related_name="roles",
        blank=True,
    )

    class Meta:
        ordering = ("name",)
        verbose_name = "Platform Role"
        verbose_name_plural = "Platform Roles"

    def __str__(self) -> str:
        return self.name

    def module_codenames(self) -> set[str]:
        """Return active module codenames granted by this role."""
        return set(
            self.modules.filter(is_active=True).values_list("codename", flat=True)
        )
