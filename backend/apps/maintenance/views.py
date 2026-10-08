from rest_framework import viewsets
from apps.users.permissions import IsFleetManager
from .models import MaintenanceRecord, MaintenanceSchedule
from .serializers import MaintenanceRecordSerializer, MaintenanceScheduleSerializer


class MaintenanceRecordViewSet(viewsets.ModelViewSet):
    """ViewSet for Maintenance Records"""
    queryset = MaintenanceRecord.objects.all()
    serializer_class = MaintenanceRecordSerializer
    permission_classes = [IsFleetManager]
    filterset_fields = ['vehicle', 'maintenance_type', 'status']
    ordering_fields = ['service_date', 'cost']


class MaintenanceScheduleViewSet(viewsets.ModelViewSet):
    """ViewSet for Maintenance Schedule"""
    queryset = MaintenanceSchedule.objects.all()
    serializer_class = MaintenanceScheduleSerializer
    permission_classes = [IsFleetManager]
    filterset_fields = ['vehicle', 'status']
