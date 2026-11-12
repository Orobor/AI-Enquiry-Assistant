import pytest

from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture
def api_client():
    """
    Provide an unauthenticated DRF API client.

    This client can make HTTP requests to API endpoints.
    """

    return APIClient()


@pytest.fixture
def test_user(db):
    """
    Create a reusable test user.

    The db fixture enables database access.
    """

    return User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="StrongPassword123!@#",
        first_name="Test",
        last_name="User",
    )


@pytest.fixture
def authenticated_client(api_client, test_user):
    """
    Return an API client authenticated as test_user.

    force_authenticate bypasses the authentication process.
    It is useful for testing protected endpoints independently
    of the login implementation.
    """

    api_client.force_authenticate(user=test_user)

    return api_client


@pytest.fixture
def valid_registration_data():
    """
    Provide valid registration data for registration tests.
    """

    return {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "AnotherStrongPassword123!@#",
    }