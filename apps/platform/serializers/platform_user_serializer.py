from rest_framework import serializers

from apps.accounts.models import User


class PlatformUserSerializer(serializers.ModelSerializer):
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
            "is_active",
        )
