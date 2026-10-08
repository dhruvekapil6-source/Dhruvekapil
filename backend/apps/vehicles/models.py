from django.db import models
from django.utils import timezone


class Vehicle(models.Model):
    """Vehicle Model"""
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('maintenance', 'Under Maintenance'),
        ('retired', 'Retired'),
    )
    
    vehicle_number = models.CharField(max_length=50, unique=True)
    vehicle_type = models.CharField(max_length=100)  # Car, Truck, Van, etc.
    registration_number = models.CharField(max_length=50, unique=True)
    insurance_provider = models.CharField(max_length=255, blank=True)
    insurance_expiry = models.DateField(null=True, blank=True)
    engine_number = models.CharField(max_length=100, blank=True)
    purchase_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    current_location = models.CharField(max_length=255, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    total_distance = models.FloatField(default=0.0)  # in km
    fuel_capacity = models.FloatField(default=50.0)  # in liters
    mileage = models.FloatField(default=0.0)  # km per liter
    owner_name = models.CharField(max_length=255, blank=True)
    registration_expiry = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'vehicles'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.vehicle_number} ({self.vehicle_type})"


class VehicleService(models.Model):
    """Track vehicle service history"""
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='services')
    service_date = models.DateField(auto_now_add=True)
    service_type = models.CharField(max_length=100)  # Oil Change, Tire Change, etc.
    description = models.TextField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    service_provider = models.CharField(max_length=255)
    odometer_reading = models.FloatField()  # km
    next_service_due = models.DateField()
    
    class Meta:
        db_table = 'vehicle_services'
        ordering = ['-service_date']
    
    def __str__(self):
        return f"{self.vehicle.vehicle_number} - {self.service_type}"
