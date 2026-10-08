from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    """Extended User Profile Model"""
    ROLE_CHOICES = (
        ('admin', 'Administrator'),
        ('fleet_manager', 'Fleet Manager'),
        ('driver', 'Driver'),
        ('customer', 'Customer'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=10, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'user_profiles'
        verbose_name_plural = 'User Profiles'
    
    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"


class AuditLog(models.Model):
    """Model to track user actions for audit purposes"""
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=255)
    model_name = models.CharField(max_length=100)
    object_id = models.IntegerField(null=True)
    changes = models.JSONField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.CharField(max_length=50, blank=True)
    
    class Meta:
        db_table = 'audit_logs'
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.user} - {self.action} - {self.timestamp}"
