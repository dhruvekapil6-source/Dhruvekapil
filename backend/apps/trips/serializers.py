from rest_framework import serializers
from .models import Trip


class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = ('id', 'trip_id', 'driver', 'vehicle', 'pickup_location',
                  'pickup_latitude', 'pickup_longitude', 'destination_location',
                  'destination_latitude', 'destination_longitude', 'distance',
                  'estimated_time', 'status', 'scheduled_date', 'scheduled_time',
                  'actual_start_time', 'actual_end_time', 'actual_distance',
                  'delay_minutes', 'notes', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at', 'actual_distance')
