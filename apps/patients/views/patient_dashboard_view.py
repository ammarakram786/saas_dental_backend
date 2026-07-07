from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.appointments.models import Appointment
from apps.billing.models import Invoice


class PatientDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        appointments = Appointment.objects.filter(patient=request.user).select_related("tenant")
        invoices = Invoice.objects.filter(patient=request.user).select_related("tenant")
        return Response(
            {
                "appointments": [
                    {
                        "id": item.id,
                        "tenant": item.tenant.name,
                        "type": item.appointment_type,
                        "status": item.status,
                        "created_at": item.created_at,
                    }
                    for item in appointments
                ],
                "invoices": [
                    {
                        "id": item.id,
                        "tenant": item.tenant.name,
                        "subtotal": item.subtotal,
                        "copay_amount": item.copay_amount,
                        "status": item.status,
                    }
                    for item in invoices
                ],
            }
        )
