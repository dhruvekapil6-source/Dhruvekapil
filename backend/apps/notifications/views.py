from rest_framework import viewsets
from apps.users.permissions import IsFleetManager
from .models import Notification, NotificationPreference
from .serializers import NotificationSerializer, NotificationPreferenceSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    """ViewSet for Notifications"""
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsFleetManager]
    filterset_fields = ['notification_type', 'is_read']
    ordering_fields = ['created_at']


class NotificationPreferenceViewSet(viewsets.ModelViewSet):
    """ViewSet for Notification Preferences"""
    queryset = NotificationPreference.objects.all()
    serializer_class = NotificationPreferenceSerializer
    permission_classes = [IsFleetManager]
