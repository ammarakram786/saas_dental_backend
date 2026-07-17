from django.contrib.auth import get_user_model
from django.db.models import Max
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.appointments.models import Appointment
from apps.common.permissions import HasTenantPermission, IsTenantMember

User = get_user_model()


class TenantPatientListView(APIView):
    """Lightweight patient list derived from appointments in the current tenant."""

    permission_classes = [IsAuthenticated, IsTenantMember, HasTenantPermission]
    required_tenant_permission = "manage_appointments"

    def get(self, request):
        tenant = getattr(request, "tenant", None)
        if tenant is None:
            return Response([])

        rows = (
            Appointment.objects.filter(tenant=tenant)
            .values("patient_id")
            .annotate(last_appointment_at=Max("created_at"))
            .order_by("-last_appointment_at")
        )
        patient_ids = [row["patient_id"] for row in rows]
        last_map = {row["patient_id"]: row["last_appointment_at"] for row in rows}
        users = User.objects.filter(id__in=patient_ids)
        by_id = {u.id: u for u in users}
        results = []
        for pid in patient_ids:
            user = by_id.get(pid)
            if not user:
                continue
            results.append(
                {
                    "id": user.id,
                    "email": user.email,
                    "username": user.username,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "last_appointment_at": last_map.get(pid),
                }
            )
        return Response({"count": len(results), "results": results})
