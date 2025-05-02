from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from Myevol_app.views import admin_logout_view

urlpatterns = [
    path('admin/logout/', admin_logout_view, name='admin_logout'),  
    path('admin/', admin.site.urls),

    # API
    path('api/', include('Myevol_app.api_urls')),  # ✅ PAS de double /api

    # Documentation de l'API
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # Vues Web (HTML)
    path('', include('Myevol_app.urls')),
]
