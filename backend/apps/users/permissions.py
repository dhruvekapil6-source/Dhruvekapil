from rest_framework.permissions import BasePermission

from .models import UserProfile


class IsFleetManager(BasePermission):
    message = 'A fleet manager role is required to access fleet operations.'

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if user.is_staff or user.is_superuser:
            return True
        try:
            profile = user.profile
        except UserProfile.DoesNotExist:
            return False
        return profile.role in {'admin', 'fleet_manager'}