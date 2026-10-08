from django.db import models
from apps.vehicles.models import Vehicle


class OptimizedRoute(models.Model):
    """Store optimized routes for multiple deliveries"""
    ALGORITHM_CHOICES = (
        ('dijkstra', 'Dijkstra'),
        ('astar', 'A*'),
        ('networkx', 'NetworkX'),
        ('ortools', 'OR-Tools'),
    )
    
    route_id = models.CharField(max_length=50, unique=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='routes')
    algorithm_used = models.CharField(max_length=20, choices=ALGORITHM_CHOICES)
    delivery_points = models.JSONField()  # List of delivery locations
    optimized_sequence = models.JSONField()  # Optimized order
    total_distance = models.FloatField()  # km
    estimated_time = models.IntegerField()  # minutes
    estimated_fuel = models.FloatField()  # liters
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2)  # currency units
    actual_distance = models.FloatField(null=True, blank=True)
    actual_fuel = models.FloatField(null=True, blank=True)
    actual_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('active', 'Active'), ('completed', 'Completed')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'optimized_routes'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Route {self.route_id}"
