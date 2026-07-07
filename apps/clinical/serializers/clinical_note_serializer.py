from rest_framework import serializers

from apps.clinical.models import ClinicalNote


class ClinicalNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicalNote
        fields = (
            "id",
            "tenant",
            "appointment",
            "dentist",
            "body",
            "is_locked",
            "locked_at",
        )
        read_only_fields = ("is_locked", "locked_at")
