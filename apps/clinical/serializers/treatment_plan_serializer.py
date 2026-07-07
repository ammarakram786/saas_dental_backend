from rest_framework import serializers

from apps.clinical.models import TreatmentPlan


class TreatmentPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = TreatmentPlan
        fields = (
            "id",
            "tenant",
            "appointment",
            "phases",
            "estimated_cost",
            "consent_signed",
            "consent_signed_at",
        )
