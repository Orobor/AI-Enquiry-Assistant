# Execute business logic and database writes

import logging

from django.contrib.auth import authenticate, login, logout

logger = logging.getLogger(__name__)

"""
The inclusion of * makes all parameters following it keyword-only arguments.
It makes the function calls more readable and prevents accidentally passing arguments in the wrong order.
"""

def authenticate_user(*, request, username, password):
    
    """
    Authenticate user using inbuilt authentication backends

    Returns:
        Authenticated User instance or None.
    """

    return authenticate(
        request=request,
        username=username,
        password=password,
    )


def login_user(*, request, user):
    
    """
    Establish an authenticated session.

    """

    login(request, user)

    logger.info(
        "User logged in. User ID: %s",
        user.id
    )


def logout_user(*, request):
    
    """
    Terminate the current authenticated session.
    """

    user_id = request.user.pk if request.user.is_authenticated else None

    logout(request)

    logger.info(
        "User logged out. User ID: %s",
        user_id
    )