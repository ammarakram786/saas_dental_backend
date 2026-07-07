from rest_framework.routers import DefaultRouter

from apps.clinical.views import ClinicalNoteViewSet, OdontogramViewSet, TreatmentPlanViewSet

app_name = "clinical"

router = DefaultRouter()
router.register("odontograms", OdontogramViewSet, basename="odontogram")
router.register("notes", ClinicalNoteViewSet, basename="clinical-note")
router.register("treatment-plans", TreatmentPlanViewSet, basename="treatment-plan")

urlpatterns = router.urls
