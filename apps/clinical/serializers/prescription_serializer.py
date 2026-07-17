from rest_framework import serializers

from apps.clinical.models import Prescription


class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = (
            "id",
            "tenant",
            "clinical_note",
            "medications",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("tenant", "created_at", "updated_at")
