import re
from rest_framework import serializers
from .models import User
from django.conf import settings

# 1. User Serializer
class UserSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'first_name', 'last_name',
            'role', 'password', 'password_confirm',
            'is_subscribed'   # ✅ added here
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'role': {'read_only': True},
            'is_subscribed': {'read_only': True},  # ❌ users can’t change it themselves
        }

    def validate_email(self, value):
        if not value.endswith('@gmail.com'):
            raise serializers.ValidationError("Only '@gmail.com' emails are allowed.")
        return value

    def validate_username(self, value):
        if len(value) < 4:
            raise serializers.ValidationError("Username must be at least 4 characters long.")
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r'[0-9]', value):
            raise serializers.ValidationError("Password must contain at least one digit.")
        return value

    def validate(self, data):
        if data.get('password') != data.get('password_confirm'):
            raise serializers.ValidationError("Passwords do not match.")
        if data['first_name'].lower() == data['last_name'].lower():
            raise serializers.ValidationError("First name and last name cannot be the same.")
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    

class UserRegisterSerializer(UserSerializer):
    """Serializer for normal resume users"""

    def create(self, validated_data):
        validated_data['role'] = User.RESUME_USER
        validated_data['is_subscribed'] = False  # enforce default
        return super().create(validated_data)

class AdminRegisterSerializer(UserSerializer):
    """Serializer for admin users"""
    secret_key = serializers.CharField(write_only=True)

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ['secret_key']

    def validate(self, data):
        # Inherit normal validation
        data = super().validate(data)

        # Validate secret key
        secret_key = data.pop('secret_key', None)
        if secret_key != settings.ADMIN_REGISTER_SECRET:
            raise serializers.ValidationError({"secret_key": "Invalid admin registration key!"})

        return data

    def create(self, validated_data):
        validated_data['role'] = User.ADMIN
        validated_data['is_subscribed'] = True   # ✅ Admins are always subscribed
        return super().create(validated_data)

