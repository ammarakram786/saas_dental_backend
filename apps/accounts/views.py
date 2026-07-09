from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.accounts.models import User
from apps.accounts.serializers import (
    EmailOrUsernameTokenObtainPairSerializer,
    UserSerializer,
)


class EmailOrUsernameTokenObtainPairView(TokenObtainPairView):
    """Obtain a JWT token pair using either a username or an email."""

    serializer_class = EmailOrUsernameTokenObtainPairSerializer


class MeView(APIView):
    """Return the currently authenticated user."""

    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        user = (
            User.objects.select_related("platform_profile", "platform_profile__role", "patient_profile")
            .prefetch_related(
                "tenant_memberships__tenant",
                "tenant_memberships__role",
            )
            .get(pk=request.user.pk)
        )
        return Response(UserSerializer(user).data)
