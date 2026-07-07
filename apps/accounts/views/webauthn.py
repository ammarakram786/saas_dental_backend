from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from apps.accounts.models import MagicLinkToken
from apps.accounts.serializers import (
    MagicLinkRequestSerializer,
    MagicLinkVerifySerializer,
    UserSerializer,
    WebAuthnBeginSerializer,
    WebAuthnFinishSerializer,
)
from apps.accounts.webauthn import (
    begin_authentication,
    begin_registration,
    finish_authentication,
    finish_registration,
)

User = get_user_model()


class WebAuthnRegisterBeginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = WebAuthnBeginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        identifier = serializer.validated_data.get("email") or serializer.validated_data.get(
            "username"
        )
        username = serializer.validated_data.get("username") or identifier
        return Response(
            begin_registration(
                identifier=identifier or username,
                display_name=serializer.validated_data.get("display_name") or username,
                username=username,
            )
        )


class WebAuthnRegisterFinishView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = WebAuthnFinishSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        identifier = serializer.validated_data.get("email") or serializer.validated_data.get(
            "username"
        )
        username = serializer.validated_data.get("username") or identifier
        email = serializer.validated_data.get("email") or ""
        user, _ = User.objects.get_or_create(
            username=username,
            defaults={"email": email, "is_active": True},
        )
        finish_registration(
            user=user,
            credential=serializer.validated_data["credential"],
            device_name=serializer.validated_data.get("device_name", ""),
        )
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


class WebAuthnAuthenticateBeginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = WebAuthnBeginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        identifier = serializer.validated_data.get("username") or serializer.validated_data.get(
            "email"
        )
        return Response(begin_authentication(identifier=identifier or ""))


class WebAuthnAuthenticateFinishView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = WebAuthnFinishSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        identifier = serializer.validated_data.get("username") or serializer.validated_data.get(
            "email"
        )
        user = finish_authentication(
            identifier=identifier or "",
            credential=serializer.validated_data["credential"],
        )
        if user is None:
            return Response(
                {"detail": "Credential verification failed."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "user": UserSerializer(user).data,
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            }
        )


class MagicLinkRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = MagicLinkRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.filter(email__iexact=serializer.validated_data["email"]).first()
        if user is None:
            return Response({"detail": "If the account exists, a link has been prepared."})

        token = MagicLinkToken.objects.create(
            user=user,
            expires_at=timezone.now() + timedelta(minutes=15),
        )
        return Response({"detail": "Magic link prepared.", "token": str(token.token)})


class MagicLinkVerifyView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = MagicLinkVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = MagicLinkToken.objects.filter(
            token=serializer.validated_data["token"]
        ).select_related("user").first()
        if token is None or not token.is_valid:
            return Response({"detail": "Link expired or invalid."}, status=status.HTTP_400_BAD_REQUEST)

        token.mark_consumed()
        refresh = RefreshToken.for_user(token.user)
        return Response(
            {
                "user": UserSerializer(token.user).data,
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            }
        )
