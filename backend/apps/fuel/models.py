from django.db import models
from apps.drivers.models import Driver
from apps.vehicles.models import Vehicle


class FuelEntry(models.Model):
    """Record fuel consumption and costs"""
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='fuel_entries')
    date = models.DateField()
    amount = models.FloatField()  # liters
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    mileage = models.FloatField()  # odometer reading in km
    fuel_station = models.CharField(max_length=255, blank=True)
    receipt_file = models.FileField(upload_to='fuel_receipts/', null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'fuel_entries'
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.vehicle.vehicle_number} - {self.date}"


class FuelAnalytics(models.Model):
    """Aggregate fuel consumption data"""
    vehicle = models.OneToOneField(Vehicle, on_delete=models.CASCADE, related_name='fuel_analytics')
    month = models.DateField()
    total_fuel = models.FloatField()  # liters
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    total_distance = models.FloatField()  # km
    average_mileage = models.FloatField()  # km per liter
    cost_per_km = models.FloatField()
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'fuel_analytics'
        unique_together = ('vehicle', 'month')
    
    def __str__(self):
        return f"{self.vehicle.vehicle_number} - {self.month}"
