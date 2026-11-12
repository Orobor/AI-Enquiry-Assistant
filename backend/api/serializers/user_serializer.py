# Serializers handle input validation

from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializes profile information.

    Username is intentionally read-only.
    """

    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
        ]

        read_only_fields = ["email"]