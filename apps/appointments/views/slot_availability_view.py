from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.appointments.models import AppointmentSlot
from apps.appointments.serializers import AppointmentSlotSerializer
from apps.tenants.models import Tenant


class SlotAvailabilityView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        tenant_slug = request.query_params.get("tenant")
        date_from = request.query_params.get("date_from")
        date_to = request.query_params.get("date_to")
        queryset = AppointmentSlot.objects.filter(is_available=True)
        if tenant_slug:
            tenant = Tenant.objects.filter(slug=tenant_slug).first()
            queryset = queryset.filter(tenant=tenant)
        if date_from:
            queryset = queryset.filter(start_time__gte=date_from)
        if date_to:
            queryset = queryset.filter(end_time__lte=date_to)
        return Response(AppointmentSlotSerializer(queryset[:100], many=True).data)
