import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from apps.tenants.models.tenant import Tenant
from apps.tenants.models.tenant_member import TenantMember
from apps.authentication.models import User
from apps.authentication.services.token_service import TokenService
import uuid

@pytest.mark.django_db
class TestRealAPITenantIsolation:
    def setup_method(self):
        self.client = APIClient()
        
        # Create users
        self.user_a_admin = User.objects.create_user(email="admin_a@test.com", password="password")
        self.user_a_dev = User.objects.create_user(email="dev_a@test.com", password="password")
        self.user_b_admin = User.objects.create_user(email="admin_b@test.com", password="password")
        
        # Create tenants
        self.tenant_a = Tenant.objects.create(
            id=uuid.uuid4(), tenant_code="tenant-a", company_name="Tenant A", 
            company_domain="tenant-a.kavan.local", owner=self.user_a_admin
        )
        self.tenant_b = Tenant.objects.create(
            id=uuid.uuid4(), tenant_code="tenant-b", company_name="Tenant B", 
            company_domain="tenant-b.kavan.local", owner=self.user_b_admin
        )
        
        # Create members with specific roles and ACTIVE status
        TenantMember.objects.create(tenant=self.tenant_a, user=self.user_a_admin, role='ADMIN', status='ACTIVE')
        TenantMember.objects.create(tenant=self.tenant_a, user=self.user_a_dev, role='DEVELOPER', status='ACTIVE')
        TenantMember.objects.create(tenant=self.tenant_b, user=self.user_b_admin, role='ADMIN', status='ACTIVE')

    def _get_jwt_for_user(self, user):
        access_token, _, _ = TokenService.generate_tokens(user)
        return access_token

    def test_tenant_a_admin_can_access_tenant_a(self):
        # 1. Login as Tenant A Admin, get JWT
        token = self._get_jwt_for_user(self.user_a_admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        # 2. Call GET /api/v1/tenants/{tenant_a_id}/ -> 200
        # Ensure HOST matches tenant domain for DomainResolver middleware
        response = self.client.get(f'/api/v1/tenants/{self.tenant_a.id}/', HTTP_HOST='tenant-a.kavan.local')
        
        assert response.status_code == 200
        assert response.data['success'] is True
        assert response.data['data']['id'] == str(self.tenant_a.id)

    def test_tenant_a_cannot_access_tenant_b(self):
        # 1. Login as Tenant A Admin, get JWT
        token = self._get_jwt_for_user(self.user_a_admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        # 2. Call GET /api/v1/tenants/{tenant_b_id}/ -> 404 (because tenant_b_id is not in Tenant A's scoped manager)
        # Even if they spoof the host, they are not a member of Tenant B
        response = self.client.get(f'/api/v1/tenants/{self.tenant_b.id}/', HTTP_HOST='tenant-b.kavan.local')
        
        # Should be 403 Forbidden or 404 Not Found (since it's completely isolated)
        assert response.status_code in [403, 404]

    def test_developer_role_denied_admin_action(self):
        # 1. Login as Tenant A Developer, get JWT
        token = self._get_jwt_for_user(self.user_a_dev)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        # 2. Developer attempting an ADMIN-only action -> 403
        response = self.client.get(f'/api/v1/tenants/{self.tenant_a.id}/', HTTP_HOST='tenant-a.kavan.local')
        
        assert response.status_code == 403
