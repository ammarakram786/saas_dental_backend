from rest_framework import serializers

from apps.appointments.models import ClinicAsset


class ClinicAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicAsset
        fields = ("id", "tenant", "name", "asset_type", "is_operational")
        read_only_fields = ("tenant",)
