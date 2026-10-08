from rest_framework import viewsets
from apps.users.permissions import IsFleetManager
from .models import OptimizedRoute
from .serializers import OptimizedRouteSerializer


class OptimizedRouteViewSet(viewsets.ModelViewSet):
    """ViewSet for Route Optimization"""
    queryset = OptimizedRoute.objects.all()
    serializer_class = OptimizedRouteSerializer
    permission_classes = [IsFleetManager]
    filterset_fields = ['status', 'vehicle', 'algorithm_used']
    ordering_fields = ['created_at', 'total_distance', 'estimated_cost']
