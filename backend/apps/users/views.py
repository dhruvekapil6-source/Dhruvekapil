import logging
from urllib.parse import urlencode

from django.conf import settings
from django.core.mail import send_mail
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import BasePermission, IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.db import transaction
from .models import UserProfile, AuditLog
from .serializers import (AuditLogSerializer, PasswordResetConfirmSerializer,
                          PasswordResetRequestSerializer, RegistrationSerializer,
                          UserProfileSerializer, UserSerializer)

logger = logging.getLogger(__name__)


def _is_fleet_admin(user):
    profile = getattr(user, 'profile', None)
    return user.is_staff or getattr(profile, 'role', None) == 'admin'


class IsFleetAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and _is_fleet_admin(request.user))


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for User management"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = User.objects.order_by('pk')
        if _is_fleet_admin(self.request.user):
            return queryset
        return queryset.filter(pk=self.request.user.pk)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            user = User.objects.create_user(
                username=serializer.validated_data['username'],
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password'],
                first_name=serializer.validated_data.get('first_name', ''),
                last_name=serializer.validated_data.get('last_name', ''),
            )
            UserProfile.objects.create(
                user=user,
                role='customer',
                phone=serializer.validated_data.get('phone', ''),
            )

        return Response(
            {'message': 'Registration successful. You can now log in.'},
            status=status.HTTP_201_CREATED,
        )
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """Get current user profile"""
        try:
            profile = request.user.profile
            serializer = UserProfileSerializer(profile)
            return Response(serializer.data)
        except UserProfile.DoesNotExist:
            return Response({'error': 'User profile not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny], url_path='password-reset/request')
    def password_reset_request(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        identifier = serializer.validated_data['identifier'].strip()
        user = User.objects.filter(email__iexact=identifier).first() or User.objects.filter(username__iexact=identifier).first()

        if user and user.is_active and user.email:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_query = urlencode({'uid': uid, 'token': token})
            reset_url = f'{settings.FRONTEND_URL.rstrip("/")}/pages/forgot-password.html?{reset_query}'
            try:
                send_mail(
                    subject='Reset your Fleet Management password',
                    message=(
                        'Use the link below to reset your password. '
                        'If you did not request this, you can ignore this email.\n\n'
                        f'{reset_url}'
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=False,
                )
            except Exception:
                logger.exception('Unable to send a password reset email')
        return Response({'message': 'If an account matches, reset instructions will be sent by email.'})

    @action(detail=False, methods=['post'], permission_classes=[AllowAny], url_path='password-reset/confirm')
    def password_reset_confirm(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user_id = force_str(urlsafe_base64_decode(serializer.validated_data['uid']))
            user = User.objects.get(pk=user_id, is_active=True)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({'detail': 'This reset link is invalid or expired.'}, status=status.HTTP_400_BAD_REQUEST)

        if not default_token_generator.check_token(user, serializer.validated_data['token']):
            return Response({'detail': 'This reset link is invalid or expired.'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(serializer.validated_data['new_password'])
        user.save(update_fields=['password'])
        return Response({'message': 'Password updated successfully. You can now log in.'})


class UserProfileViewSet(viewsets.ModelViewSet):
    """ViewSet for User Profile management"""
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if _is_fleet_admin(user):
            return UserProfile.objects.all()
        return UserProfile.objects.filter(user=user)


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Audit Log (Read-only)"""
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    permission_classes = [IsFleetAdmin]
    filterset_fields = ['user', 'model_name', 'timestamp']
    ordering_fields = ['timestamp']
