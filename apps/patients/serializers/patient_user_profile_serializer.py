from rest_framework import serializers

from apps.accounts.models import PatientUserProfile


class PatientUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientUserProfile
        fields = (
            "id",
            "date_of_birth",
            "cnic",
            "primary_phone",
            "blood_type",
            "systemic_conditions",
            "allergies",
            "active_medications",
        )
