import pytest
from django.urls import reverse
from rest_framework import status

@pytest.mark.django_db
class TestEmailVerificationAPI:
    def setup_method(self):
        self.verify_url = reverse('api_v1:auth:verify-email')

    def test_verify_email_success(self, client):
        data = {"token": "valid_email_verification_token"}
        response = client.post(self.verify_url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert "verified successfully" in response.data["message"]

    def test_verify_email_invalid(self, client):
        # Empty or missing token
        data = {}
        response = client.post(self.verify_url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
