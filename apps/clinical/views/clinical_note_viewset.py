from rest_framework import status
from rest_framework.response import Response

from apps.clinical.filters import ClinicalNoteFilter
from apps.clinical.models import ClinicalNote
from apps.clinical.serializers import ClinicalNoteSerializer
from apps.common.viewsets import BaseTenantViewSet


class ClinicalNoteViewSet(BaseTenantViewSet):
    queryset = ClinicalNote.objects.select_related("appointment", "dentist")
    serializer_class = ClinicalNoteSerializer
    required_tenant_permission = "edit_clinical_chart"

    filterset_class = ClinicalNoteFilter
    search_fields = ["dentist__username"]
    ordering_fields = ["id", "created_at", "locked_at", "is_locked"]

    def update(self, request, *args, **kwargs):
        if self.get_object().is_locked:
            return Response(
                {"detail": "Locked notes cannot be edited."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if self.get_object().is_locked:
            return Response(
                {"detail": "Locked notes cannot be deleted."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().destroy(request, *args, **kwargs)
