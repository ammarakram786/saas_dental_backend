from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from apps.accounts.models import PlatformUserProfile, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("username", "email", "is_staff", "is_superuser", "is_active")
    list_filter = ("is_staff", "is_superuser", "is_active")
    search_fields = ("username", "email", "first_name", "last_name")
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Security", {"fields": ("last_login_ip",)}),
    )


@admin.register(PlatformUserProfile)
class PlatformUserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "is_super_admin", "contact_phone", "created_at")
    list_filter = ("is_super_admin", "role")
    autocomplete_fields = ("user", "role")
    search_fields = ("user__username", "user__email")
