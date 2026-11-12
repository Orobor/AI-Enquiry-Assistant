# Serializers handle input validation

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

User = get_user_model()


class RegistrationSerializer(serializers.Serializer):
    
    """
    Validates user registration data.

    Passwords are write-only and are never included in API responses.
    """

    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)
    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True,
        trim_whitespace=False
    )

    def validate_email(self, value):
        
        """Ensure that the email is not already registered."""

        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Email already exists."
            )

        return value

    def validate_password(self, value):
        
        """Apply Django's configured password validation rules."""

        validate_password(value)
        
        return value


class LoginSerializer(serializers.Serializer):
    
    """Validates login credentials."""

    username = serializers.CharField()
    password = serializers.CharField(
        write_only=True,
        trim_whitespace=False
    )

