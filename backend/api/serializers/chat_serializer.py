
from rest_framework import serializers


class ChatSerializer(serializers.Serializer):
    
    """ Validates user message """
    message = serializers.CharField(
        required=True,
        allow_blank=False,
        trim_whitespace=True,
        max_length=500,
        error_messages={
            "required": "Message is required.",
            "blank": "Message cannot be empty.",
            "max_length": "Message cannot exceed 500 characters.",
        }
    )
