from rest_framework import viewsets
from apps.users.permissions import IsFleetManager
from .models import FuelEntry, FuelAnalytics
from .serializers import FuelEntrySerializer, FuelAnalyticsSerializer


class FuelEntryViewSet(viewsets.ModelViewSet):
    """ViewSet for Fuel Entry"""
    queryset = FuelEntry.objects.all()
    serializer_class = FuelEntrySerializer
    permission_classes = [IsFleetManager]
    filterset_fields = ['vehicle', 'driver', 'date']
    ordering_fields = ['date', 'cost']


class FuelAnalyticsViewSet(viewsets.ModelViewSet):
    """ViewSet for Fuel Analytics"""
    queryset = FuelAnalytics.objects.all()
    serializer_class = FuelAnalyticsSerializer
    permission_classes = [IsFleetManager]
    filterset_fields = ['vehicle', 'month']
