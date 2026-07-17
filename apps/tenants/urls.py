from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.tenants.views import (
    MePermissionsView,
    TenantMembershipViewSet,
    TenantPatientListView,
    TenantRoleViewSet,
)

app_name = "tenants"

router = DefaultRouter()
router.register("memberships", TenantMembershipViewSet, basename="tenant-membership")
router.register("roles", TenantRoleViewSet, basename="tenant-role")

urlpatterns = [
    path("me/permissions/", MePermissionsView.as_view(), name="me-permissions"),
    path("patients/", TenantPatientListView.as_view(), name="tenant-patients"),
]
urlpatterns += router.urls
