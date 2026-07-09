from rest_framework import serializers

from apps.accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    is_super_admin = serializers.SerializerMethodField()
    platform_role = serializers.SerializerMethodField()
    platform_modules = serializers.SerializerMethodField()
    workspaces = serializers.SerializerMethodField()
    actor_types = serializers.SerializerMethodField()

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
            "actor_types",
            "is_staff",
            "is_active",
        )
        read_only_fields = fields

    def _platform_profile(self, obj):
        return getattr(obj, "platform_profile", None)

    def get_is_super_admin(self, obj):
        profile = self._platform_profile(obj)
        return profile.is_super_admin if profile else False

    def get_platform_role(self, obj):
        profile = self._platform_profile(obj)
        return profile.role_id if profile else None

    def get_platform_modules(self, obj):
        profile = self._platform_profile(obj)
        if profile is None:
            return []
        return sorted(profile.module_codenames())

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

    def get_actor_types(self, obj):
        actor_types = []
        profile = self._platform_profile(obj)
        if profile and (profile.is_super_admin or profile.role_id):
            actor_types.append("platform")
        if obj.tenant_memberships.filter(is_active=True).exists():
            actor_types.append("tenant")
        if getattr(obj, "patient_profile", None) is not None:
            actor_types.append("patient")
        return actor_types
