from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from apps.users.permissions import IsFleetManager
from django.db.models import Sum, Count, Avg
from apps.vehicles.models import Vehicle
from apps.trips.models import Trip
from apps.drivers.models import Driver
from apps.fuel.models import FuelEntry, FuelAnalytics
from apps.maintenance.models import MaintenanceRecord


class DashboardViewSet(viewsets.ViewSet):
    """ViewSet for Dashboard analytics"""
    permission_classes = [IsFleetManager]
    
    def list(self, request):
        """Get dashboard summary statistics"""
        # Vehicle Statistics
        total_vehicles = Vehicle.objects.count()
        active_vehicles = Vehicle.objects.filter(status='active').count()
        maintenance_vehicles = Vehicle.objects.filter(status='maintenance').count()
        
        # Trip Statistics
        total_trips = Trip.objects.count()
        active_trips = Trip.objects.filter(status='in_progress').count()
        completed_trips = Trip.objects.filter(status='completed').count()
        total_distance = Trip.objects.filter(status='completed').aggregate(Sum('actual_distance'))['actual_distance__sum'] or 0
        
        # Driver Statistics
        total_drivers = Driver.objects.count()
        active_drivers = Driver.objects.filter(status='active').count()
        avg_driver_rating = Driver.objects.aggregate(Avg('rating'))['rating__avg'] or 0
        
        # Fuel Statistics
        total_fuel_cost = FuelEntry.objects.aggregate(Sum('cost'))['cost__sum'] or 0
        total_fuel_consumed = FuelEntry.objects.aggregate(Sum('amount'))['amount__sum'] or 0
        
        # Maintenance Statistics
        maintenance_count = MaintenanceRecord.objects.filter(status='completed').count()
        maintenance_cost = MaintenanceRecord.objects.filter(status='completed').aggregate(Sum('cost'))['cost__sum'] or 0
        
        data = {
            'vehicles': {
                'total': total_vehicles,
                'active': active_vehicles,
                'maintenance': maintenance_vehicles,
            },
            'trips': {
                'total': total_trips,
                'active': active_trips,
                'completed': completed_trips,
                'total_distance': total_distance,
            },
            'drivers': {
                'total': total_drivers,
                'active': active_drivers,
                'average_rating': round(avg_driver_rating, 2),
            },
            'fuel': {
                'total_cost': float(total_fuel_cost),
                'total_consumed': total_fuel_consumed,
            },
            'maintenance': {
                'completed': maintenance_count,
                'total_cost': float(maintenance_cost),
            },
        }
        
        return Response(data)
