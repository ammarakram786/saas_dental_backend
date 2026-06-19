from django.contrib import admin

from apps.tenants.models import (
    Tenant,
    TenantMembership,
    TenantPermission,
    TenantRole,
)


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(TenantPermission)
class TenantPermissionAdmin(admin.ModelAdmin):
    list_display = ("codename", "name", "is_active")
    list_filter = ("is_active",)
    search_fields = ("codename", "name", "description")
    prepopulated_fields = {"codename": ("name",)}


@admin.register(TenantRole)
class TenantRoleAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "tenant", "is_system", "is_active")
    list_filter = ("is_system", "is_active", "tenant")
    search_fields = ("name", "slug", "tenant__slug")
    filter_horizontal = ("permissions",)
    autocomplete_fields = ("tenant",)


@admin.register(TenantMembership)
class TenantMembershipAdmin(admin.ModelAdmin):
    list_display = ("user", "tenant", "role", "is_active")
    list_filter = ("is_active", "tenant")
    search_fields = ("user__username", "user__email", "tenant__slug")
    autocomplete_fields = ("user", "tenant", "role")
