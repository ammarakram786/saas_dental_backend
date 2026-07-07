from rest_framework import serializers

from apps.platform.models import PlatformAuditEvent


class PlatformAuditSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlatformAuditEvent
        fields = ("id", "actor", "action", "target", "severity", "category", "created_at")
