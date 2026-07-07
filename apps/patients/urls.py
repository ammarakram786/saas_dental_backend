from django.urls import path

from apps.patients.views import PatientDashboardView, PatientMedicalProfileView

app_name = "patients"

urlpatterns = [
    path("dashboard/", PatientDashboardView.as_view(), name="dashboard"),
    path("medical-profile/", PatientMedicalProfileView.as_view(), name="medical-profile"),
]
