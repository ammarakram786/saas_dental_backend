from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.appointments.views import (
    AppointmentSlotViewSet,
    AppointmentViewSet,
    ClinicAssetViewSet,
    PatientAppointmentViewSet,
    SlotAvailabilityView,
)

app_name = "appointments"

router = DefaultRouter()
router.register("appointments", AppointmentViewSet, basename="appointment")
router.register("patient", PatientAppointmentViewSet, basename="patient-appointment")
router.register("slots", AppointmentSlotViewSet, basename="appointment-slot")
router.register("assets", ClinicAssetViewSet, basename="clinic-asset")

urlpatterns = [
    path("availability/", SlotAvailabilityView.as_view(), name="availability"),
]
urlpatterns += router.urls
