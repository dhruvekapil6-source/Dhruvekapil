from django.db import models


class Report(models.Model):
    """Generate reports in different formats"""
    REPORT_TYPE_CHOICES = (
        ('vehicle', 'Vehicle Report'),
        ('driver', 'Driver Report'),
        ('fuel', 'Fuel Report'),
        ('trip', 'Trip Report'),
        ('maintenance', 'Maintenance Report'),
        ('financial', 'Financial Report'),
    )
    
    FORMAT_CHOICES = (
        ('pdf', 'PDF'),
        ('excel', 'Excel'),
        ('csv', 'CSV'),
    )
    
    report_type = models.CharField(max_length=20, choices=REPORT_TYPE_CHOICES)
    format = models.CharField(max_length=10, choices=FORMAT_CHOICES)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    filters = models.JSONField(null=True, blank=True)  # Store filter criteria
    file_path = models.FileField(upload_to='reports/', null=True, blank=True)
    generated_by = models.CharField(max_length=255)
    total_records = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('processing', 'Processing'), ('completed', 'Completed'), ('failed', 'Failed')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    generated_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'reports'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_report_type_display()} - {self.created_at}"
