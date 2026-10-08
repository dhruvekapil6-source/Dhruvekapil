from django.db import models
from django.contrib.auth.models import User


class Notification(models.Model):
    """Send notifications to users"""
    TYPE_CHOICES = (
        ('service_due', 'Service Due'),
        ('insurance_expiry', 'Insurance Expiry'),
        ('license_expiry', 'License Expiry'),
        ('trip_delay', 'Trip Delay'),
        ('fuel_low', 'Fuel Low'),
        ('maintenance_reminder', 'Maintenance Reminder'),
        ('system_alert', 'System Alert'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=30, choices=TYPE_CHOICES)
    title = models.CharField(max_length=255)
    message = models.TextField()
    related_object_id = models.IntegerField(null=True, blank=True)
    related_object_type = models.CharField(max_length=100, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'notifications'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"


class NotificationPreference(models.Model):
    """User notification preferences"""
    CHANNEL_CHOICES = (
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('in_app', 'In-App'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='notification_preference')
    email_enabled = models.BooleanField(default=True)
    sms_enabled = models.BooleanField(default=False)
    in_app_enabled = models.BooleanField(default=True)
    service_due_notification = models.BooleanField(default=True)
    insurance_expiry_notification = models.BooleanField(default=True)
    license_expiry_notification = models.BooleanField(default=True)
    trip_delay_notification = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'notification_preferences'
    
    def __str__(self):
        return f"Notification Preferences - {self.user.username}"
