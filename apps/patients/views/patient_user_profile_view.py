from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.models import PatientUserProfile
from apps.patients.serializers.patient_user_profile_serializer import (
    PatientUserProfileSerializer,
)


class PatientUserProfileView(APIView):
    """GET/PATCH the authenticated patient's account profile (phone, DOB, etc.)."""

    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj, _ = PatientUserProfile.objects.get_or_create(user=self.request.user)
        return obj

    def get(self, request):
        return Response(PatientUserProfileSerializer(self.get_object()).data)

    def patch(self, request):
        serializer = PatientUserProfileSerializer(
            self.get_object(),
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
