import pytest
from django.urls import reverse
from rest_framework import status
from apps.authentication.models import User

@pytest.mark.django_db
class TestPasswordReset:
    def setup_method(self):
        self.forgot_password_url = reverse('api_v1:auth:forgot-password')
        self.reset_password_url = reverse('api_v1:auth:reset-password')
        self.user = User.objects.create_user(email="reset@example.com", password="SecurePassword123!")

    def test_forgot_password_success(self, client):
        data = {"email": "reset@example.com"}
        response = client.post(self.forgot_password_url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert "sent" in response.data.get("message", "").lower()

    def test_reset_password_invalid_token(self, client):
        data = {
            "token": "invalid_token",
            "password": "NewSecurePassword123!",
            "confirm_password": "NewSecurePassword123!"
        }
        response = client.post(self.reset_password_url, data, format='json')
        # Assuming our service rejects it
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_reset_password_mismatch(self, client):
        data = {
            "token": "some_token",
            "password": "NewSecurePassword123!",
            "confirm_password": "DifferentPassword123!"
        }
        response = client.post(self.reset_password_url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
