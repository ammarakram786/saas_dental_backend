from rest_framework import serializers

from apps.platform.models import PlatformModule, PlatformRole


class PlatformModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlatformModule
        fields = ("id", "codename", "name", "description", "is_active")


class PlatformRoleSerializer(serializers.ModelSerializer):
    modules = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=PlatformModule.objects.all(),
        required=False,
    )
    module_codenames = serializers.SerializerMethodField()

    class Meta:
        model = PlatformRole
        fields = (
            "id",
            "name",
            "slug",
            "description",
            "is_active",
            "modules",
            "module_codenames",
        )

    def get_module_codenames(self, obj):
        return sorted(obj.module_codenames())
