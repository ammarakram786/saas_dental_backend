from rest_framework import serializers

from apps.billing.models import Invoice


class PlatformBillingSerializer(serializers.ModelSerializer):
    tenant_name = serializers.CharField(source="tenant.name", read_only=True)

    class Meta:
        model = Invoice
        fields = (
            "id",
            "tenant",
            "tenant_name",
            "patient",
            "subtotal",
            "insurance_coverage",
            "copay_amount",
            "status",
            "created_at",
        )
