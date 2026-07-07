from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.accounts.urls')),
    path('api/platform/', include('apps.platform.urls')),
    path('api/tenant/', include('apps.tenants.urls')),
    path('api/scheduling/', include('apps.appointments.urls')),
    path('api/patient/', include('apps.patients.urls')),
    path('api/clinical/', include('apps.clinical.urls')),
    path('api/billing/', include('apps.billing.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
