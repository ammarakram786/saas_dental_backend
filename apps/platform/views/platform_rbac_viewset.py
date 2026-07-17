from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from apps.common.permissions import HasPlatformModuleAccess
from apps.platform.models import PlatformModule, PlatformRole
from apps.platform.serializers.platform_rbac_serializer import (
    PlatformModuleSerializer,
    PlatformRoleSerializer,
)


class PlatformModuleViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = PlatformModule.objects.filter(is_active=True)
    serializer_class = PlatformModuleSerializer
    permission_classes = [IsAuthenticated, HasPlatformModuleAccess]
    required_module_codename = "manage_tenants"
    search_fields = ["codename", "name"]
    ordering_fields = ["codename", "name"]


class PlatformRoleViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = PlatformRole.objects.prefetch_related("modules")
    serializer_class = PlatformRoleSerializer
    permission_classes = [IsAuthenticated, HasPlatformModuleAccess]
    required_module_codename = "manage_tenants"
    search_fields = ["name", "slug"]
    ordering_fields = ["name", "slug"]
