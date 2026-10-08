from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OptimizedRouteViewSet

router = DefaultRouter()
router.register(r'', OptimizedRouteViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
