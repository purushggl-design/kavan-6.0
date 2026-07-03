import pytest
from django.urls import reverse
from rest_framework import status

@pytest.mark.django_db
class TestOAuthAPI:
    def setup_method(self):
        self.oauth_url = reverse('api_v1:auth:oauth-login')

    def test_oauth_login(self, client):
        data = {"provider": "google", "token": "mock_google_token"}
        response = client.post(self.oauth_url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert "access_token" in response.data["data"]
