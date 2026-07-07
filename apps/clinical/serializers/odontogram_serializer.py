from rest_framework import serializers

from apps.clinical.models import Odontogram


class OdontogramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Odontogram
        fields = ("id", "tenant", "appointment", "tooth_map")
