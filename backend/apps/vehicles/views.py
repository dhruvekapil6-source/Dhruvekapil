from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.users.permissions import IsFleetManager
from .models import Vehicle, VehicleService
from .serializers import VehicleSerializer, VehicleServiceSerializer


class VehicleViewSet(viewsets.ModelViewSet):
    """ViewSet for Vehicle management"""
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [IsFleetManager]
    filterset_fields = ['status', 'vehicle_type']
    search_fields = ['vehicle_number', 'registration_number']
    ordering_fields = ['created_at', 'vehicle_number']
    
    @action(detail=True, methods=['post'])
    def update_location(self, request, pk=None):
        """Update vehicle location"""
        vehicle = self.get_object()
        latitude = request.data.get('latitude')
        longitude = request.data.get('longitude')
        current_location = request.data.get('current_location')
        
        if latitude is not None:
            vehicle.latitude = latitude
        if longitude is not None:
            vehicle.longitude = longitude
        if current_location:
            vehicle.current_location = current_location
        
        vehicle.save()
        return Response(VehicleSerializer(vehicle).data)
    
    @action(detail=True, methods=['get'])
    def services(self, request, pk=None):
        """Get vehicle service history"""
        vehicle = self.get_object()
        services = vehicle.services.all()
        serializer = VehicleServiceSerializer(services, many=True)
        return Response(serializer.data)


class VehicleServiceViewSet(viewsets.ModelViewSet):
    """ViewSet for Vehicle Service management"""
    queryset = VehicleService.objects.all()
    serializer_class = VehicleServiceSerializer
    permission_classes = [IsFleetManager]
    filterset_fields = ['vehicle', 'service_type']
    ordering_fields = ['service_date']
