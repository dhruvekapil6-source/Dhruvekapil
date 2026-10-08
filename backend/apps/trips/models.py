from django.db import models
from apps.drivers.models import Driver
from apps.vehicles.models import Vehicle


class Trip(models.Model):
    """Trip Model"""
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('assigned', 'Assigned'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('delayed', 'Delayed'),
    )
    
    trip_id = models.CharField(max_length=50, unique=True)
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True)
    pickup_location = models.CharField(max_length=255)
    pickup_latitude = models.FloatField()
    pickup_longitude = models.FloatField()
    destination_location = models.CharField(max_length=255)
    destination_latitude = models.FloatField()
    destination_longitude = models.FloatField()
    distance = models.FloatField()  # in km
    estimated_time = models.IntegerField()  # in minutes
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    scheduled_date = models.DateField()
    scheduled_time = models.TimeField()
    actual_start_time = models.DateTimeField(null=True, blank=True)
    actual_end_time = models.DateTimeField(null=True, blank=True)
    actual_distance = models.FloatField(null=True, blank=True)
    delay_minutes = models.IntegerField(default=0)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'trips'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Trip {self.trip_id} - {self.driver}"
