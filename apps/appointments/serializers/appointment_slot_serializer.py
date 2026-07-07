from rest_framework import serializers

from apps.appointments.models import AppointmentSlot


class AppointmentSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppointmentSlot
        fields = (
            "id",
            "tenant",
            "dentist",
            "chair",
            "start_time",
            "end_time",
            "is_available",
        )
