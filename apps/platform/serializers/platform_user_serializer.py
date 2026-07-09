from rest_framework import serializers

from apps.accounts.models import PlatformUserProfile
from apps.platform.models import PlatformRole


class PlatformUserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="user.id", read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    is_active = serializers.BooleanField(source="user.is_active", read_only=True)
    platform_role = serializers.PrimaryKeyRelatedField(
        source="role",
        queryset=PlatformRole.objects.all(),
        allow_null=True,
        required=False,
    )

    class Meta:
        model = PlatformUserProfile
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "is_super_admin",
            "platform_role",
            "is_active",
            "contact_phone",
        )
