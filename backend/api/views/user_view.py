# Handle HTTP requests and responses
import json
from django.views.decorators.csrf import csrf_protect

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from api.serializers.user_serializer import ProfileSerializer
from api.selectors.user_selectors import get_user_profile
from api.services.user_service import update_user_profile

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def dashboard(request):
    
    """
    Return dashboard information for the authenticated user.

    Anonymous users cannot access this endpoint.
    """

    user = request.user

    context = {
        "message": "Welcome to Dashboard",
        "user": {
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
        }
    }

    return Response(context, status=status.HTTP_200_OK)

@api_view(["GET", "PUT"])
@permission_classes([IsAuthenticated])
def profile(request):
    
    """
    GET:
        Retrieve the authenticated user's profile.

    PUT:
        Validate and update the authenticated user's profile.
    """

    user = request.user

    # Retrieve existing profile information.
    if request.method == "GET":

        return Response(
            get_user_profile(user)
        )

    # Validate incoming profile information.
    serializer = ProfileSerializer(
        user,
        data=request.data,
        partial=True
    )

    serializer.is_valid(raise_exception=True)

    # Delegate database updates to the service layer.
    updated_user = update_user_profile(
        user=user,
        validated_data=serializer.validated_data,
    )

    context = {
        "message": "Profile updated successfully",
        "user": {
            "username": updated_user.username,
            "email": updated_user.email,
            "first_name": updated_user.first_name,
            "last_name": updated_user.last_name,
        }
    }

    return Response(context, status=status.HTTP_200_OK)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def active_user(request):
    
    """
    Restore the authenticated user when the React
    application refreshes or reloads.

    The frontend uses this endpoint to determine whether
    an existing Django session is still valid.
    """

    user = request.user

    context = {
        "message": True,
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
        }
    }

    return Response(context, status=status.HTTP_200_OK)



