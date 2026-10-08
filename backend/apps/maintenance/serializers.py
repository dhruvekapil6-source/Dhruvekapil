from rest_framework import serializers
from .models import MaintenanceRecord, MaintenanceSchedule


class MaintenanceRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceRecord
        fields = ('id', 'vehicle', 'maintenance_type', 'description', 'service_provider',
                  'cost', 'service_date', 'completion_date', 'parts_replaced',
                  'labor_cost', 'parts_cost', 'odometer_reading', 'status', 'created_at')
        read_only_fields = ('id', 'created_at')


class MaintenanceScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceSchedule
        fields = ('id', 'vehicle', 'last_service_date', 'next_service_date',
                  'service_interval_km', 'service_interval_days', 'last_odometer',
                  'status', 'updated_at')
        read_only_fields = ('id', 'updated_at')
