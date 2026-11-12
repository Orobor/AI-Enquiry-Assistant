# Handle HTTP requests and responses

import logging

from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_protect

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from api.serializers.auth_serializer import RegistrationSerializer, LoginSerializer
from api.services.user_service import create_user
from api.services.auth_service import authenticate_user, login_user, logout_user

logger = logging.getLogger(__name__)


@api_view(["GET"])
@permission_classes([AllowAny])
def csrf_token(request):
    """
    Generate or retrieve a CSRF token.

    React should call this endpoint before submitting
    requests that require CSRF protection.
    """

    return Response({
        "csrfToken": get_token(request)
    })


@csrf_protect
@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    
    """
    Register a new user account.

    """

    # Validate the incoming registration data
    serializer = RegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    try:
        # Create the user through the service layer
        user = create_user(
            first_name=serializer.validated_data["first_name"],
            last_name=serializer.validated_data["last_name"],
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"]
        )

    except Exception:
        logger.exception("Unexpected user registration failure.")

        return Response(
            {"error": "Unable to complete registration."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    # Return the newly created username
    return Response(
        { "message": "Registration successful!"},
        status=status.HTTP_201_CREATED
    )


@csrf_protect
@api_view(["POST"])
@permission_classes([AllowAny])
def user_login(request):
    
    """
    Authenticate a user and establish a session.

    Invalid credentials return HTTP 401.
    """

    # Validate the incoming login data
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    # Authenticate the user through the service layer
    user = authenticate_user(
        request=request,
        username=serializer.validated_data["username"],
        password=serializer.validated_data["password"],
    )

    # If authentication fails, log the attempt and return an error response.
    if user is None:
        logger.warning("Failed login attempt.")

        return Response(
            {"error": "Invalid username or password"},
            status=status.HTTP_401_UNAUTHORIZED
        )

    # If authentication succeeds, log the user in and return a success response.
    login_user(
        request=request,
        user=user
    )

    return Response(
        {"message": "Login successful!"},
        status=status.HTTP_200_OK
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def user_logout(request):
    
    """
    Log out the authenticated user and destroy their session.
    """

    # Delegate the logout operation to the service layer.
    logout_user(request=request)

    return Response(
        {"message": "Logged out successfully!"},
        status=status.HTTP_200_OK
    )