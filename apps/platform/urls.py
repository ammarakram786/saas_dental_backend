from rest_framework.routers import DefaultRouter

from apps.platform.views import (
    AuditLogViewSet,
    BillingViewSet,
    PlatformUserViewSet,
    TenantViewSet,
)

app_name = "platform"

router = DefaultRouter()
router.register("tenants", TenantViewSet, basename="platform-tenant")
router.register("team", PlatformUserViewSet, basename="platform-team")
router.register("billing", BillingViewSet, basename="platform-billing")
router.register("audit", AuditLogViewSet, basename="platform-audit")

urlpatterns = router.urls
