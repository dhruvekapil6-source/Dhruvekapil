from rest_framework import serializers
from .models import Notification, NotificationPreference


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('id', 'user', 'notification_type', 'title', 'message',
                  'related_object_id', 'related_object_type', 'is_read',
                  'created_at', 'read_at')
        read_only_fields = ('id', 'created_at')


class NotificationPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationPreference
        fields = ('id', 'user', 'email_enabled', 'sms_enabled', 'in_app_enabled',
                  'service_due_notification', 'insurance_expiry_notification',
                  'license_expiry_notification', 'trip_delay_notification')
        read_only_fields = ('id',)
