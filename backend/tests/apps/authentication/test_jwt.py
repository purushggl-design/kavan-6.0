import pytest
from django.urls import reverse
from rest_framework import status
from apps.authentication.models import User
from apps.authentication.services.token_service import TokenService

@pytest.mark.django_db
class TestJWTAndRefresh:
    def setup_method(self):
        self.refresh_url = reverse('api_v1:auth:refresh')
        self.user = User.objects.create_user(email="jwt@example.com", password="SecurePassword123!")
        self.access, self.refresh, _ = TokenService.generate_tokens(self.user, ip_address="127.0.0.1")

    def test_refresh_token_success(self, client):
        data = {"refresh_token": self.refresh}
        response = client.post(self.refresh_url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert "access_token" in response.data.get("data", {})
        assert "refresh_token" in response.data.get("data", {})

    def test_refresh_token_invalid(self, client):
        data = {"refresh_token": "invalid_refresh_token_string"}
        response = client.post(self.refresh_url, data, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_refresh_token_blacklisted(self, client):
        # Simulate logout / blacklist
        token_hash = TokenService._hash_token(self.refresh)
        from apps.authentication.models import RefreshToken
        RefreshToken.objects.filter(token_hash=token_hash).update(is_revoked=True)
        
        data = {"refresh_token": self.refresh}
        response = client.post(self.refresh_url, data, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
