from rest_framework import serializers
from .models import Driver


class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ('id', 'user', 'driver_id', 'license_number', 'license_class',
                  'license_expiry', 'phone', 'address', 'city', 'state', 'country',
                  'postal_code', 'experience_years', 'date_of_birth', 'assigned_vehicle',
                  'status', 'total_trips', 'total_distance', 'rating', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at', 'total_trips', 'total_distance')
