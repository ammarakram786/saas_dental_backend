from rest_framework.routers import DefaultRouter

from apps.billing.views import InsurancePanelViewSet, InvoiceViewSet, PaymentRecordViewSet

app_name = "billing"

router = DefaultRouter()
router.register("invoices", InvoiceViewSet, basename="invoice")
router.register("payments", PaymentRecordViewSet, basename="payment")
router.register("insurance-panels", InsurancePanelViewSet, basename="insurance-panel")

urlpatterns = router.urls
