from rest_framework import viewsets
from apps.users.permissions import IsFleetManager
from .models import Driver
from .serializers import DriverSerializer


class DriverViewSet(viewsets.ModelViewSet):
    """ViewSet for Driver management"""
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    permission_classes = [IsFleetManager]
    filterset_fields = ['status', 'license_class']
    search_fields = ['driver_id', 'user__first_name', 'user__last_name']
    ordering_fields = ['created_at', 'rating', 'total_trips']
