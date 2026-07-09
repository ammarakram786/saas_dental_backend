from rest_framework import serializers

from apps.tenants.models import Tenant
from apps.tenants.services import TenantProvisioningError, provision_tenant_with_admin


class TenantAdminUserInputSerializer(serializers.Serializer):
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=150, required=False, allow_blank=True, default="")
    last_name = serializers.CharField(max_length=150, required=False, allow_blank=True, default="")
    password = serializers.CharField(
        write_only=True,
        required=False,
        allow_blank=True,
        min_length=8,
        trim_whitespace=False,
    )


class TenantSerializer(serializers.ModelSerializer):
    admin_user = TenantAdminUserInputSerializer(write_only=True, required=False)

    class Meta:
        model = Tenant
        fields = (
            "id",
            "name",
            "slug",
            "is_active",
            "created_at",
            "updated_at",
            "admin_user",
        )
        read_only_fields = ("id", "created_at", "updated_at")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance is not None:
            self.fields.pop("admin_user", None)

    def validate(self, attrs):
        if self.instance is None and "admin_user" not in attrs:
            raise serializers.ValidationError(
                {"admin_user": "Admin user details are required when creating a tenant."}
            )
        return attrs

    def create(self, validated_data):
        admin_data = validated_data.pop("admin_user")
        try:
            result = provision_tenant_with_admin(
                name=validated_data["name"],
                slug=validated_data["slug"],
                is_active=validated_data.get("is_active", True),
                admin_email=admin_data["email"],
                admin_first_name=admin_data.get("first_name", ""),
                admin_last_name=admin_data.get("last_name", ""),
                admin_password=admin_data.get("password") or None,
            )
        except TenantProvisioningError as exc:
            raise serializers.ValidationError(exc.detail) from exc

        tenant = result.tenant
        tenant._provisioned_admin_user = {
            "id": result.admin_user.pk,
            "email": result.admin_user.email,
            "first_name": result.admin_user.first_name,
            "last_name": result.admin_user.last_name,
            "created": result.created_user,
        }
        return tenant

    def to_representation(self, instance):
        data = super().to_representation(instance)
        provisioned = getattr(instance, "_provisioned_admin_user", None)
        if provisioned is not None:
            data["admin_user"] = provisioned
        return data
