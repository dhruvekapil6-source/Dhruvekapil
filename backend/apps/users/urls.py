from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, UserProfileViewSet, AuditLogViewSet

router = DefaultRouter()
router.register(r'profiles', UserProfileViewSet)
router.register(r'audit-logs', AuditLogViewSet)
router.register(r'', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
