from apps.accounts.filters import PlatformUserFilter
from apps.accounts.models import PlatformUserProfile
from apps.common.viewsets import BasePlatformViewSet
from apps.platform.serializers import PlatformUserSerializer


class PlatformUserViewSet(BasePlatformViewSet):
    queryset = PlatformUserProfile.objects.select_related("user", "role").all()
    serializer_class = PlatformUserSerializer
    required_module_codename = "manage_tenants"

    filterset_class = PlatformUserFilter
    search_fields = [
        "user__username",
        "user__email",
        "user__first_name",
        "user__last_name",
    ]
    ordering_fields = ["id", "user__username", "user__email", "created_at"]
