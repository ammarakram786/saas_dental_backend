from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from apps.accounts.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("username", "email", "is_super_admin", "platform_role", "is_staff", "is_active")
    list_filter = ("is_super_admin", "is_staff", "is_active")
    autocomplete_fields = ("platform_role",)
    search_fields = ("username", "email", "first_name", "last_name")
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Platform", {"fields": ("is_super_admin", "platform_role", "last_login_ip")}),
    )
