import pytest

from rest_framework import status

PROFILE_URL = "/api/profile/"
ACTIVE_USER_URL = "/api/active_user/"


@pytest.mark.django_db
@pytest.mark.profile
class TestProfile:
    """Tests for profile retrieval and updates."""

    def test_get_profile(self, authenticated_client):
        """Authenticated users should retrieve their profile."""

        response = authenticated_client.get(PROFILE_URL)

        assert response.status_code == status.HTTP_200_OK

        assert response.data == {
            "username": "testuser",
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
        }

    def test_update_profile(self, authenticated_client, test_user):
        """Users should be able to update their profile."""

        response = authenticated_client.put(
            PROFILE_URL,
            {
                "email": "updated@example.com",
                "first_name": "Updated",
                "last_name": "Name",
            },
            format="json"
        )

        assert response.status_code == status.HTTP_200_OK

        assert response.data["message"] == "Profile updated successfully"

        test_user.refresh_from_db()

        assert test_user.email == "updated@example.com"
        assert test_user.first_name == "Updated"
        assert test_user.last_name == "Name"

    def test_partial_profile_update(self, authenticated_client, test_user):
        """Only supplied fields should be updated."""

        response = authenticated_client.put(
            PROFILE_URL,
            {
                "first_name": "Updated",
            },
            format="json"
        )

        assert response.status_code == status.HTTP_200_OK

        test_user.refresh_from_db()

        assert test_user.first_name == "Updated"
        assert test_user.last_name == "User"
        assert test_user.email == "test@example.com"

    def test_invalid_email(self, authenticated_client):
        """Invalid email addresses should be rejected."""

        response = authenticated_client.put(
            PROFILE_URL,
            {
                "email": "invalid-email",
            },
            format="json"
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_profile_requires_authentication(self, api_client):
        """Anonymous users should not retrieve profiles."""

        response = api_client.get(PROFILE_URL)

        assert response.status_code in (
            status.HTTP_401_UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN,
        )

    def test_active_user(self, authenticated_client):
        """Active user endpoint should return authenticated user data."""

        response = authenticated_client.get(ACTIVE_USER_URL)

        assert response.status_code == status.HTTP_200_OK

        assert response.data["success"] is True
        assert response.data["username"] == "testuser"
        assert response.data["email"] == "test@example.com"

    def test_active_user_requires_authentication(self, api_client):
        """Anonymous users cannot restore an authenticated session."""

        response = api_client.get(ACTIVE_USER_URL)

        assert response.status_code in (
            status.HTTP_401_UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN,
        )