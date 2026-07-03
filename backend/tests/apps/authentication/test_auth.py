import pytest
from django.urls import reverse
from rest_framework import status
from apps.authentication.models import User

@pytest.mark.django_db
class TestAuthentication:
    def setup_method(self):
        self.register_url = reverse('api_v1:auth:register')
        self.login_url = reverse('api_v1:auth:login')
        self.valid_user_data = {
            "email": "test@example.com",
            "password": "SecurePassword123!",
            "confirm_password": "SecurePassword123!",
            "first_name": "Test",
            "last_name": "User"
        }

    def test_user_registration_success(self, client):
        response = client.post(self.register_url, self.valid_user_data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.filter(email="test@example.com").exists()

    def test_user_registration_password_mismatch(self, client):
        data = self.valid_user_data.copy()
        data['confirm_password'] = "DifferentPassword123!"
        response = client.post(self.register_url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_user_login_success(self, client):
        # Register user first
        User.objects.create_user(email="test@example.com", password="SecurePassword123!")
        
        login_data = {
            "email": "test@example.com",
            "password": "SecurePassword123!"
        }
        response = client.post(self.login_url, login_data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert "access_token" in response.data.get("data", {})

    def test_user_login_invalid_credentials(self, client):
        login_data = {
            "email": "test@example.com",
            "password": "WrongPassword!"
        }
        response = client.post(self.login_url, login_data, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
