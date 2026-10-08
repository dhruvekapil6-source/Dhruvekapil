from django.db import models
from django.contrib.auth.models import User
from apps.vehicles.models import Vehicle


class Driver(models.Model):
    """Driver Model"""
    LICENSE_CLASS_CHOICES = (
        ('A', 'Class A - Motorcycle'),
        ('B', 'Class B - Car'),
        ('C', 'Class C - Truck'),
        ('D', 'Class D - Bus'),
        ('LMV', 'LMV - Light Motor Vehicle'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='driver')
    driver_id = models.CharField(max_length=50, unique=True)
    license_number = models.CharField(max_length=100, unique=True)
    license_class = models.CharField(max_length=10, choices=LICENSE_CLASS_CHOICES)
    license_expiry = models.DateField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)
    experience_years = models.IntegerField(default=0)
    date_of_birth = models.DateField()
    assigned_vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('active', 'Active'), ('inactive', 'Inactive'), ('on_leave', 'On Leave')], default='active')
    total_trips = models.IntegerField(default=0)
    total_distance = models.FloatField(default=0.0)
    rating = models.FloatField(default=0.0)  # 0-5 stars
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'drivers'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.first_name} ({self.driver_id})"
