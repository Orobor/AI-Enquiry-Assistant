import pytest

from rest_framework import status

DASHBOARD_URL = "/api/dashboard/"


@pytest.mark.django_db
class TestDashboard:
    """Tests for the authenticated dashboard."""

    def test_authenticated_dashboard(self, authenticated_client):
        """Authenticated users should access the dashboard."""

        response = authenticated_client.get(DASHBOARD_URL)

        assert response.status_code == status.HTTP_200_OK

        assert response.data["message"] == "Welcome to Dashboard"

        assert response.data["user"]["username"] == "testuser"

        assert response.data["user"]["email"] == "test@example.com"

    def test_anonymous_dashboard_access(self, api_client):
        """Anonymous users should not access the dashboard."""

        response = api_client.get(DASHBOARD_URL)

        assert response.status_code in (
            status.HTTP_401_UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN,
        )