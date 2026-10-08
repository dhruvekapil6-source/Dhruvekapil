from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MaintenanceRecordViewSet, MaintenanceScheduleViewSet

router = DefaultRouter()
router.register(r'records', MaintenanceRecordViewSet)
router.register(r'schedule', MaintenanceScheduleViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
