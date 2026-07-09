import pytest
from django.urls import reverse
from rest_framework import status
from apps.authentication.models import User
from apps.authentication.services.token_service import TokenService

@pytest.mark.django_db
class TestMFA:
    def setup_method(self):
        self.mfa_setup_url = reverse('api_v1:auth:mfa-setup')
        self.mfa_verify_url = reverse('api_v1:auth:mfa-verify')
        self.user = User.objects.create_user(email="mfa@example.com", password="SecurePassword123!")
        self.access, _, _ = TokenService.generate_tokens(self.user, ip_address="127.0.0.1")
        self.auth_headers = {"HTTP_AUTHORIZATION": f"Bearer {self.access}"}

    def test_mfa_setup(self, client):
        response = client.post(self.mfa_setup_url, **self.auth_headers)
        assert response.status_code == status.HTTP_200_OK
        assert "otp_uri" in response.data.get("data", {})

    def test_mfa_verify_invalid_otp(self, client):
        data = {"otp": "123456"} # assuming dummy always fails unless mocked
        response = client.post(self.mfa_verify_url, data, format='json', **self.auth_headers)
        # Since we use real MFA now, a fake OTP without setup will fail setup verification
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_mfa_verify_invalid_format(self, client):
        data = {"otp": "12A"} # invalid format
        response = client.post(self.mfa_verify_url, data, format='json', **self.auth_headers)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
