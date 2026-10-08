from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VehicleViewSet, VehicleServiceViewSet

router = DefaultRouter()
router.register(r'', VehicleViewSet)
router.register(r'services', VehicleServiceViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
