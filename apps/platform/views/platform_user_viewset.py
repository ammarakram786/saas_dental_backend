from apps.accounts.filters import UserFilter
from apps.accounts.models import User
from apps.common.viewsets import BasePlatformViewSet
from apps.platform.serializers import PlatformUserSerializer


class PlatformUserViewSet(BasePlatformViewSet):
    queryset = User.objects.select_related("platform_role").all()
    serializer_class = PlatformUserSerializer
    required_module_codename = "manage_tenants"

    filterset_class = UserFilter
    search_fields = ["username", "email", "first_name", "last_name"]
    ordering_fields = ["id", "username", "email", "date_joined"]
