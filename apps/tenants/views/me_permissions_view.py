from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class MePermissionsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tenant = getattr(request, "tenant", None)
        if tenant is None:
            return Response({"tenant": None, "permissions": []})

        role = request.user.tenant_role(tenant)
        permissions = sorted(role.permission_codenames()) if role else []
        return Response(
            {
                "tenant": tenant.pk,
                "tenant_slug": tenant.slug,
                "role": getattr(role, "slug", None),
                "permissions": permissions,
            }
        )
