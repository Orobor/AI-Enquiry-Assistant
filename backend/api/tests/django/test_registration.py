import pytest

from django.contrib.auth import get_user_model
from rest_framework import status

User = get_user_model()

REGISTER_URL = "/api/register/"


@pytest.mark.django_db
@pytest.mark.auth
class TestRegistration:
    """Tests for the user registration endpoint."""

    def test_successful_registration(
        self,
        api_client,
        valid_registration_data
    ):
        """A valid user should be registered successfully."""

        response = api_client.post(
            REGISTER_URL,
            valid_registration_data,
            format="json"
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["message"] == "Registration successful"
        assert response.data["username"] == "newuser"

        user = User.objects.get(username="newuser")

        assert user.email == "newuser@example.com"
        assert user.check_password(
            valid_registration_data["password"]
        )

    def test_duplicate_username(
        self,
        api_client,
        test_user,
        valid_registration_data
    ):
        """Registration should reject an existing username."""

        response = api_client.post(
            REGISTER_URL,
            {
                **valid_registration_data,
                "username": test_user.username,
            },
            format="json"
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.parametrize(
        "missing_field",
        ["username", "email", "password"]
    )
    def test_missing_required_fields(
        self,
        api_client,
        valid_registration_data,
        missing_field
    ):
        """Registration should reject missing required fields."""

        data = valid_registration_data.copy()
        data.pop(missing_field)

        response = api_client.post(
            REGISTER_URL,
            data,
            format="json"
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_invalid_email(
        self,
        api_client,
        valid_registration_data
    ):
        """Registration should reject invalid email addresses."""

        data = {
            **valid_registration_data,
            "email": "invalid-email",
        }

        response = api_client.post(
            REGISTER_URL,
            data,
            format="json"
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_weak_password(
        self,
        api_client,
        valid_registration_data
    ):
        """Registration should reject weak passwords."""

        data = {
            **valid_registration_data,
            "password": "123",
        }

        response = api_client.post(
            REGISTER_URL,
            data,
            format="json"
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST