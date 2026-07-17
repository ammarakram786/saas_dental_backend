from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("apps.accounts.urls")),
    path("api/platform/", include("apps.platform.urls")),
    path("api/tenant/", include("apps.tenants.urls")),
    path("api/scheduling/", include("apps.appointments.urls")),
    path("api/patient/", include("apps.patients.urls")),
    path("api/clinical/", include("apps.clinical.urls")),
    path("api/billing/", include("apps.billing.urls")),
]

if settings.DEBUG or getattr(settings, "ENABLE_API_DOCS", False):
    urlpatterns += [
        path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
        path(
            "api/docs/",
            SpectacularSwaggerView.as_view(url_name="schema"),
            name="swagger-ui",
        ),
        path(
            "api/redoc/",
            SpectacularRedocView.as_view(url_name="schema"),
            name="redoc",
        ),
    ]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
