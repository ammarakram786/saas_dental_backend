from rest_framework import serializers

from apps.accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    platform_modules = serializers.SerializerMethodField()
    workspaces = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "is_super_admin",
            "platform_role",
            "platform_modules",
            "workspaces",
            "is_staff",
            "is_active",
        )
        read_only_fields = fields

    def get_platform_modules(self, obj):
        if obj.is_super_admin:
            from apps.platform.models import PlatformModule

            return list(
                PlatformModule.objects.filter(is_active=True).values_list(
                    "codename", flat=True
                )
            )
        role = obj.platform_role
        return sorted(role.module_codenames()) if role and role.is_active else []

    def get_workspaces(self, obj):
        return [
            {
                "id": membership.tenant_id,
                "name": membership.tenant.name,
                "subdomain": membership.tenant.slug,
                "role": membership.role.slug,
            }
            for membership in obj.tenant_memberships.select_related("tenant", "role").filter(
                is_active=True
            )
        ]
