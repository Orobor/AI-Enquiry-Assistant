# Handle HTTP requests and responses

import logging

from django.views.decorators.csrf import csrf_protect

from rest_framework.throttling import UserRateThrottle
from rest_framework.decorators import throttle_classes

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from api.serializers.chat_serializer import ChatSerializer

from api.agent.agent_workflow import AgentWorkflow

logger = logging.getLogger(__name__)

# Controls how many requests a user can make to your API within a specific period of time
class ChatRateThrottle(UserRateThrottle):
    rate = "30/minute" # Maximum of 30 requests per minute

# Instantiate AgentWorkflow
agent = AgentWorkflow()   

@csrf_protect
@api_view(["POST"])
@permission_classes([IsAuthenticated])
@throttle_classes([ChatRateThrottle])
def chat(request):
    """
    Handle authenticated user chat requests. 
    
    Applies rate limiting to prevent excessive API usage.

    Returns:
        Response:
            200 OK: Message successfully processed with chatbot response.
            500 Internal Server Error: Unexpected chatbot processing failure.
    """

    # Authenticated user
    user = request.user

    # Validate incoming data
    serializer = ChatSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    message = serializer.validated_data["message"]
    
    try:
        
        # Chatbot processing logic
        response = agent.ask(question=message)

        return Response(
            {"response": response['answer']},
            status=status.HTTP_200_OK
        )

    except Exception:
        logger.exception(
            "Unexpected chatbot processing failure. User ID: %s",
            request.user.id
        )

        return Response(
            {"error": "Unable to process your message."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
