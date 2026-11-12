# Retrieve data from the database

from django.contrib.auth import get_user_model

User = get_user_model()


def get_user_by_id(user_id: int):
    
    """
    Retrieve a user using their primary key.

    Returns:
        User instance or None.
    """

    return User.objects.filter(id=user_id).first()


def get_user_by_username(username: str):
    
    """
    Retrieve a user using their username.

    Returns:
        User instance or None.
    """

    return User.objects.filter(username=username).first()


def get_user_profile(user):
    
    """
    Retrieve profile information for an authenticated user.
    """

    return {
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
    }