from apps.common.viewsets import BasePlatformViewSet
from apps.platform.filters import PlatformAuditEventFilter
from apps.platform.models import PlatformAuditEvent
from apps.platform.serializers import PlatformAuditSerializer


class AuditLogViewSet(BasePlatformViewSet):
    queryset = PlatformAuditEvent.objects.all()
    serializer_class = PlatformAuditSerializer
    required_module_codename = "security_audit"

    filterset_class = PlatformAuditEventFilter
    search_fields = ["actor", "action", "target"]
    ordering_fields = ["id", "created_at", "severity", "category"]
