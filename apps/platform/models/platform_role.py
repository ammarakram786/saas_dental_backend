from django.db import models

from apps.common.models import TimeStampedModel


class PlatformRole(TimeStampedModel):
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=150, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    modules = models.ManyToManyField(
        "platform.PlatformModule",
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
        return set(
            self.modules.filter(is_active=True).values_list("codename", flat=True)
        )
