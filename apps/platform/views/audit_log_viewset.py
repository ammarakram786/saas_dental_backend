from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated

from apps.common.permissions import HasPlatformModuleAccess
from apps.platform.filters import PlatformAuditEventFilter
from apps.platform.models import PlatformAuditEvent
from apps.platform.serializers import PlatformAuditSerializer


class AuditLogViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """Read-only audit log for platform operators."""

    queryset = PlatformAuditEvent.objects.all()
    serializer_class = PlatformAuditSerializer
    permission_classes = [IsAuthenticated, HasPlatformModuleAccess]
    required_module_codename = "security_audit"
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    filterset_class = PlatformAuditEventFilter
    search_fields = ["actor", "action", "target"]
    ordering_fields = ["id", "created_at", "severity", "category"]
