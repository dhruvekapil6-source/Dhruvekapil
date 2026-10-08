from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FuelEntryViewSet, FuelAnalyticsViewSet

router = DefaultRouter()
router.register(r'entries', FuelEntryViewSet)
router.register(r'analytics', FuelAnalyticsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
