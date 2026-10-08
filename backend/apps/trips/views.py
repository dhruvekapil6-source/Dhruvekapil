from rest_framework import viewsets
from apps.users.permissions import IsFleetManager
from .models import Trip
from .serializers import TripSerializer


class TripViewSet(viewsets.ModelViewSet):
    """ViewSet for Trip management"""
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    permission_classes = [IsFleetManager]
    filterset_fields = ['status', 'driver', 'vehicle', 'scheduled_date']
    search_fields = ['trip_id', 'pickup_location', 'destination_location']
    ordering_fields = ['created_at', 'scheduled_date', 'distance']
