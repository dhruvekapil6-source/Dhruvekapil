from django.db import models
from apps.vehicles.models import Vehicle


class MaintenanceRecord(models.Model):
    """Track vehicle maintenance history"""
    TYPE_CHOICES = (
        ('routine', 'Routine Maintenance'),
        ('repair', 'Repair'),
        ('inspection', 'Inspection'),
        ('replacement', 'Replacement'),
        ('other', 'Other'),
    )
    
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='maintenance_records')
    maintenance_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    description = models.TextField()
    service_provider = models.CharField(max_length=255)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    service_date = models.DateField()
    completion_date = models.DateField(null=True, blank=True)
    parts_replaced = models.JSONField(null=True, blank=True)  # List of parts
    labor_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    parts_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    odometer_reading = models.FloatField()
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('in_progress', 'In Progress'), ('completed', 'Completed')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'maintenance_records'
        ordering = ['-service_date']
    
    def __str__(self):
        return f"{self.vehicle.vehicle_number} - {self.maintenance_type}"


class MaintenanceSchedule(models.Model):
    """Predict and schedule maintenance"""
    vehicle = models.OneToOneField(Vehicle, on_delete=models.CASCADE, related_name='maintenance_schedule')
    last_service_date = models.DateField()
    next_service_date = models.DateField()
    service_interval_km = models.IntegerField()  # km between services
    service_interval_days = models.IntegerField()  # days between services
    last_odometer = models.FloatField()
    status = models.CharField(max_length=20, choices=[('ok', 'OK'), ('due_soon', 'Due Soon'), ('overdue', 'Overdue')], default='ok')
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'maintenance_schedules'
    
    def __str__(self):
        return f"Maintenance Schedule - {self.vehicle.vehicle_number}"
