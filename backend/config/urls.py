"""
URL configuration for fleet_management project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.views.static import serve
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from apps.users.serializers import FleetTokenObtainPairSerializer


class FleetTokenObtainPairView(TokenObtainPairView):
    serializer_class = FleetTokenObtainPairSerializer

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='dashboard.html'), name='frontend-home'),
    path('pages/dashboard.html', TemplateView.as_view(template_name='dashboard.html'), name='frontend-dashboard'),
    path('pages/login.html', TemplateView.as_view(template_name='login.html'), name='frontend-login'),
    path('pages/register.html', TemplateView.as_view(template_name='register.html'), name='frontend-register'),
    path('pages/forgot-password.html', TemplateView.as_view(template_name='forgot-password.html'), name='frontend-forgot-password'),
    path('pages/vehicles.html', TemplateView.as_view(template_name='vehicles.html'), name='frontend-vehicles'),
    path('api/token/', FleetTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # API URLs
    path('api/users/', include('apps.users.urls')),
    path('api/vehicles/', include('apps.vehicles.urls')),
    path('api/drivers/', include('apps.drivers.urls')),
    path('api/trips/', include('apps.trips.urls')),
    path('api/routes/', include('apps.routes.urls')),
    path('api/fuel/', include('apps.fuel.urls')),
    path('api/maintenance/', include('apps.maintenance.urls')),
    path('api/notifications/', include('apps.notifications.urls')),
    path('api/reports/', include('apps.reports.urls')),
    path('api/dashboard/', include('apps.dashboard.urls')),
    path('css/<path:path>', serve, {'document_root': settings.PROJECT_ROOT / 'frontend' / 'css'}),
    path('js/<path:path>', serve, {'document_root': settings.PROJECT_ROOT / 'frontend' / 'js'}),
    path('assets/<path:path>', serve, {'document_root': settings.PROJECT_ROOT / 'frontend' / 'assets'}),
]

for page_name in (
    'drivers',
    'trips',
    'routes',
    'fuel',
    'maintenance',
    'reports',
    'notifications',
    'profile',
    'trip-details',
):
    urlpatterns.append(
        path(
            f'pages/{page_name}.html',
            TemplateView.as_view(
                template_name='operations.html',
                extra_context={'module': page_name},
            ),
            name=f'frontend-{page_name}',
        )
    )

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
