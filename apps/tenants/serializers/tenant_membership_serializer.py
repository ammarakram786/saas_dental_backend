from rest_framework import serializers

from apps.tenants.models import TenantMembership


class TenantMembershipSerializer(serializers.ModelSerializer):
    role_name = serializers.CharField(source="role.name", read_only=True)
    user_display = serializers.SerializerMethodField()

    class Meta:
        model = TenantMembership
        fields = (
            "id",
            "user",
            "user_display",
            "tenant",
            "role",
            "role_name",
            "is_active",
        )

    def get_user_display(self, obj):
        full_name = f"{obj.user.first_name} {obj.user.last_name}".strip()
        return full_name or obj.user.username
