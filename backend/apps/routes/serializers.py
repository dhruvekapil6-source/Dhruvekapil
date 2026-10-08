from rest_framework import serializers
from .models import OptimizedRoute


class OptimizedRouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = OptimizedRoute
        fields = ('id', 'route_id', 'vehicle', 'algorithm_used', 'delivery_points',
                  'optimized_sequence', 'total_distance', 'estimated_time',
                  'estimated_fuel', 'estimated_cost', 'actual_distance',
                  'actual_fuel', 'actual_cost', 'status', 'created_at', 'completed_at')
        read_only_fields = ('id', 'created_at')
