from rest_framework import serializers

from apps.billing.models import PaymentRecord


class PaymentRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentRecord
        fields = (
            "id",
            "tenant",
            "invoice",
            "method",
            "amount",
            "gateway_ref",
            "gateway_status",
            "created_at",
        )
