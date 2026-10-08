from rest_framework import serializers
from .models import Vehicle, VehicleService


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ('id', 'vehicle_number', 'vehicle_type', 'registration_number',
                  'insurance_provider', 'insurance_expiry', 'engine_number',
                  'purchase_date', 'status', 'current_location', 'latitude',
                  'longitude', 'total_distance', 'fuel_capacity', 'mileage',
                  'registration_expiry', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')


class VehicleServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleService
        fields = ('id', 'vehicle', 'service_date', 'service_type', 'description',
                  'cost', 'service_provider', 'odometer_reading', 'next_service_due')
        read_only_fields = ('id', 'service_date')
