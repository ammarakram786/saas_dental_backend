from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)

from apps.accounts.views import (
    EmailOrUsernameTokenObtainPairView,
    MagicLinkRequestView,
    MagicLinkVerifyView,
    MeView,
    WebAuthnAuthenticateBeginView,
    WebAuthnAuthenticateFinishView,
    WebAuthnRegisterBeginView,
    WebAuthnRegisterFinishView,
)

app_name = "accounts"

urlpatterns = [
    path("token/", EmailOrUsernameTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("me/", MeView.as_view(), name="me"),
    path("webauthn/register/begin/", WebAuthnRegisterBeginView.as_view(), name="webauthn_register_begin"),
    path("webauthn/register/finish/", WebAuthnRegisterFinishView.as_view(), name="webauthn_register_finish"),
    path("webauthn/authenticate/begin/", WebAuthnAuthenticateBeginView.as_view(), name="webauthn_authenticate_begin"),
    path("webauthn/authenticate/finish/", WebAuthnAuthenticateFinishView.as_view(), name="webauthn_authenticate_finish"),
    path("magic-link/request/", MagicLinkRequestView.as_view(), name="magic_link_request"),
    path("magic-link/verify/", MagicLinkVerifyView.as_view(), name="magic_link_verify"),
]
