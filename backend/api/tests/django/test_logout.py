import pytest

from rest_framework import status

LOGOUT_URL = "/api/logout/"
DASHBOARD_URL = "/api/dashboard/"


@pytest.mark.django_db
@pytest.mark.auth
class TestLogout:
    """Tests for user logout."""

    def test_successful_logout(self, authenticated_client):
        """Authenticated users should be able to log out."""

        response = authenticated_client.post(LOGOUT_URL)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["message"] == "Logged out successfully!"

        # The user should no longer access protected endpoints.
        dashboard_response = authenticated_client.get(DASHBOARD_URL)

        assert dashboard_response.status_code in (
            status.HTTP_401_UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN,
        )

    def test_logout_requires_authentication(self, api_client):
        """Anonymous users should not access logout."""

        response = api_client.post(LOGOUT_URL)

        assert response.status_code in (
            status.HTTP_401_UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN,
        )