from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from rest_framework.permissions import IsAdminUser

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('API.urls')),

    # OpenAPI schema
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),

    # Swagger UI (admin only)
    path(
        'api/schema/swagger-ui/',
        SpectacularSwaggerView.as_view(url_name='schema', permission_classes=[IsAdminUser]),
        name='swagger-ui'
    ),

    # Redoc UI (admin only)
    path(
        'api/schema/redoc/',
        SpectacularRedocView.as_view(url_name='schema', permission_classes=[IsAdminUser]),
        name='redoc'
    ),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
