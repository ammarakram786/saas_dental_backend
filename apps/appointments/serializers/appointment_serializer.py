from rest_framework import serializers

from apps.appointments.models import Appointment


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = (
            "id",
            "tenant",
            "patient",
            "slot",
            "status",
            "appointment_type",
            "notes",
            "created_at",
        )
