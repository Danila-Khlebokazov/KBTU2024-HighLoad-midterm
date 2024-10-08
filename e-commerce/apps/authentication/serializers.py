from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import User


class RegistrationSerializer(serializers.ModelSerializer):
    """Serialization of user registration and creating."""

    password = serializers.CharField(max_length=128, min_length=8, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ["phone_number", "username", "password", "token"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    """Serialization of user login."""

    phone_number = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        phone_number = data.get("phone_number", None)
        password = data.get("password", None)
        if phone_number is None:
            raise serializers.ValidationError("A phone number is required to log in.")
        if password is None:
            raise serializers.ValidationError("A password is required to log in.")
        user = authenticate(username=phone_number, password=password)
        if user is None:
            raise serializers.ValidationError("A user with this email and password was not found.")
        if not user.is_active:
            raise serializers.ValidationError("This user has been deactivated.")
        return {"phone_number": user.phone_number, "username": user.username, "token": user.token}


class UserSerializer(serializers.ModelSerializer):
    """User object serialization."""

    password = serializers.CharField(max_length=128, min_length=8, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = (
            "phone_number",
            "username",
            "password",
            "token",
        )

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for key, value in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
