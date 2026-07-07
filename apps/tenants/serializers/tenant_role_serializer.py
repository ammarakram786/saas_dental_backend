from rest_framework import serializers

from apps.tenants.models import TenantRole


class TenantRoleSerializer(serializers.ModelSerializer):
    permission_codenames = serializers.SlugRelatedField(
        source="permissions",
        slug_field="codename",
        many=True,
        read_only=True,
    )

    class Meta:
        model = TenantRole
        fields = (
            "id",
            "tenant",
            "name",
            "slug",
            "description",
            "is_system",
            "is_active",
            "permission_codenames",
        )
