from rest_framework import serializers

from apps.billing.models import InsurancePanel


class InsurancePanelSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsurancePanel
        fields = ("id", "tenant", "insurer_name", "panel_code", "coverage_rules")
