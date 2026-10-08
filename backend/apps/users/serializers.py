from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import UserProfile, AuditLog


class RegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    first_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    last_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    phone = serializers.CharField(max_length=20, required=False, allow_blank=True)

    def validate_username(self, value):
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError('Username is already in use.')
        return value


class PasswordResetRequestSerializer(serializers.Serializer):
    identifier = serializers.CharField(max_length=254)


class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True, min_length=8)


class FleetTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        identifier = attrs.get('username', '').strip()
        user = User.objects.filter(email__iexact=identifier).first()
        if user:
            attrs['username'] = user.username
        else:
            matching_user = User.objects.filter(username__iexact=identifier).first()
            if matching_user:
                attrs['username'] = matching_user.username
        return super().validate(attrs)

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError('Email is already registered.')
        return value


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')
        read_only_fields = ('id',)


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ('id', 'user', 'role', 'phone', 'address', 'city', 'state', 
                  'country', 'postal_code', 'profile_picture', 'is_active')
        read_only_fields = ('id', 'user', 'role', 'is_active')


class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = ('id', 'user', 'action', 'model_name', 'object_id', 'changes', 'timestamp')
        read_only_fields = ('id', 'timestamp')
