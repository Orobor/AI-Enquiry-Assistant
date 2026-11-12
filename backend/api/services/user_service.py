# Execute business logic and database writes

import logging

from django.contrib.auth import get_user_model
from django.db import IntegrityError

User = get_user_model()

logger = logging.getLogger(__name__)

"""
The inclusion of * makes all parameters following it keyword-only arguments.
It makes the function calls more readable and prevents accidentally passing arguments in the wrong order.
"""

def create_user(*, first_name, last_name, email, password):
    """
    Create a new user account.

    Args:
        last_name: User's last name.
        first_name: User's first name.
        email: User email address.
        username: User's username.
        password: Raw password.

    Returns:
        Newly created User instance.

    Raises:
        IntegrityError: If a database constraint is violated.

    """

    try:

        # Create a new user instance and save it to the database.
        user = User.objects.create_user(
            
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=email,
            password=password,

        )

        logger.info(
            "New user account created. User ID: %s",
            user.id
        )

        return user

    except IntegrityError:

        logger.exception(
            "User registration failed due to a database constraint."
        )
        raise


def update_user_profile(*, user, validated_data):
    """Update and return the authenticated user's profile."""

    try:

        # Update the user's profile information in the database.
        User.objects.filter(pk=user.pk).update(
            first_name=validated_data.get("first_name", user.first_name),
            last_name=validated_data.get("last_name", user.last_name),
        )

        # Refresh the user instance to reflect the latest changes from the database.
        user.refresh_from_db()

        logger.info("User profile updated. User ID: %s", user.id)

    except IntegrityError:
        
        logger.exception(
            "User profile update failed due to a database constraint. User ID: %s",
            user.id
        )
        raise

    return user