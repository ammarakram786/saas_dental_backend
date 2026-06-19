from django.contrib import admin

from apps.platform.models import PlatformModule, PlatformRole


@admin.register(PlatformModule)
class PlatformModuleAdmin(admin.ModelAdmin):
    list_display = ("codename", "name", "is_active", "updated_at")
    list_filter = ("is_active",)
    search_fields = ("codename", "name", "description")
    prepopulated_fields = {"codename": ("name",)}


@admin.register(PlatformRole)
class PlatformRoleAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_active", "updated_at")
    list_filter = ("is_active",)
    search_fields = ("name", "slug", "description")
    prepopulated_fields = {"slug": ("name",)}
    filter_horizontal = ("modules",)
