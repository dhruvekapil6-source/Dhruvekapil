from rest_framework import serializers
from .models import FuelEntry, FuelAnalytics


class FuelEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = FuelEntry
        fields = ('id', 'driver', 'vehicle', 'date', 'amount', 'cost', 'mileage',
                  'fuel_station', 'receipt_file', 'notes', 'created_at')
        read_only_fields = ('id', 'created_at')


class FuelAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FuelAnalytics
        fields = ('id', 'vehicle', 'month', 'total_fuel', 'total_cost', 'total_distance',
                  'average_mileage', 'cost_per_km', 'updated_at')
        read_only_fields = ('id', 'updated_at')
