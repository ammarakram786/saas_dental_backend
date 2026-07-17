from rest_framework import serializers

from apps.billing.models import Invoice


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = (
            "id",
            "tenant",
            "appointment",
            "patient",
            "line_items",
            "subtotal",
            "insurance_coverage",
            "copay_amount",
            "status",
            "created_at",
        )
        read_only_fields = ("tenant", "created_at")
