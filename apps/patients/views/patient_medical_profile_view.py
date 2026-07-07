from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.models import PatientUserProfile
from apps.patients.models import PatientMedicalProfile
from apps.patients.serializers import PatientMedicalProfileSerializer


class PatientMedicalProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        patient_profile = PatientUserProfile.objects.get(user=self.request.user)
        obj, _ = PatientMedicalProfile.objects.get_or_create(patient=patient_profile)
        return obj

    def get(self, request):
        return Response(PatientMedicalProfileSerializer(self.get_object()).data)

    def patch(self, request):
        serializer = PatientMedicalProfileSerializer(
            self.get_object(),
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
