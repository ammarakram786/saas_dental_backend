from rest_framework import serializers

from apps.accounts.models import User


class UserSerializer(serializers.ModelSerializer):
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
            "is_staff",
            "is_active",
        )
        read_only_fields = fields
