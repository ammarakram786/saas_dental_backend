from django.db import models

from apps.common.models import TimeStampedModel


class PlatformUserProfile(TimeStampedModel):
    user = models.OneToOneField(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="platform_profile",
    )
    role = models.ForeignKey(
        "platform.PlatformRole",
        null=True,
        blank=True,
        default=None,
        on_delete=models.SET_NULL,
        related_name="platform_users",
        help_text="Control-plane role for this platform operator.",
    )
    is_super_admin = models.BooleanField(
        default=False,
        help_text="Bypasses all platform and tenant RBAC constraints.",
    )
    contact_phone = models.CharField(max_length=30, blank=True)
    avatar = models.ImageField(upload_to="avatars/platform/", blank=True, null=True)

    class Meta:
        verbose_name = "Platform User"
        verbose_name_plural = "Platform Users"

    def __str__(self) -> str:
        return f"PlatformProfile<{self.user_id}>"

    def module_codenames(self) -> set[str]:
        if self.is_super_admin:
            from apps.platform.models import PlatformModule

            return set(
                PlatformModule.objects.filter(is_active=True).values_list(
                    "codename", flat=True
                )
            )
        role = self.role
        if role is None or not role.is_active:
            return set()
        return role.module_codenames()

    def has_module(self, codename: str) -> bool:
        if self.is_super_admin:
            return True
        role = self.role
        if role is None or not role.is_active:
            return False

        from apps.common.cache import get_platform_role_modules

        return codename in get_platform_role_modules(role)
