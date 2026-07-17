import django_filters

from apps.clinical.models import Prescription


class PrescriptionFilter(django_filters.FilterSet):
    patient = django_filters.NumberFilter(
        field_name="clinical_note__appointment__patient_id"
    )
    appointment = django_filters.NumberFilter(
        field_name="clinical_note__appointment_id"
    )

    class Meta:
        model = Prescription
        fields = ["clinical_note"]
