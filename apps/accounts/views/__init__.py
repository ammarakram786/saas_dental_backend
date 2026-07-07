from .me import MeView
from .token import EmailOrUsernameTokenObtainPairView
from .webauthn import (
    MagicLinkRequestView,
    MagicLinkVerifyView,
    WebAuthnAuthenticateBeginView,
    WebAuthnAuthenticateFinishView,
    WebAuthnRegisterBeginView,
    WebAuthnRegisterFinishView,
)

__all__ = [
    "EmailOrUsernameTokenObtainPairView",
    "MagicLinkRequestView",
    "MagicLinkVerifyView",
    "MeView",
    "WebAuthnAuthenticateBeginView",
    "WebAuthnAuthenticateFinishView",
    "WebAuthnRegisterBeginView",
    "WebAuthnRegisterFinishView",
]
