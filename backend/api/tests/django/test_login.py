import pytest

from rest_framework import status

LOGIN_URL = "/api/login/"


@pytest.mark.django_db
@pytest.mark.auth
class TestLogin:
    """Tests for user authentication."""

    def test_successful_login(
        self,
        api_client,
        test_user
    ):
        """Valid credentials should establish a session."""

        response = api_client.post(
            LOGIN_URL,
            {
                "username": "testuser",
                "password": "StrongPassword123!@#",
            },
            format="json"
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["message"] == "Login successful"

        # Verify that Django created an authenticated session.
        assert "_auth_user_id" in api_client.session

    def test_invalid_password(
        self,
        api_client,
        test_user
    ):
        """Incorrect passwords should be rejected."""

        response = api_client.post(
            LOGIN_URL,
            {
                "username": "testuser",
                "password": "wrongpassword",
            },
            format="json"
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_nonexistent_user(self, api_client):
        """Nonexistent users should not authenticate."""

        response = api_client.post(
            LOGIN_URL,
            {
                "username": "unknownuser",
                "password": "SomePassword123!",
            },
            format="json"
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_missing_credentials(self, api_client):
        """Login should reject missing credentials."""

        response = api_client.post(
            LOGIN_URL,
            {},
            format="json"
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST