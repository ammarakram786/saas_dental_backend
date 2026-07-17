from rest_framework import serializers

from apps.patients.models import PatientMedicalProfile


class PatientMedicalProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientMedicalProfile
        fields = ("id", "patient", "global_health_notes")
        read_only_fields = ("patient",)
