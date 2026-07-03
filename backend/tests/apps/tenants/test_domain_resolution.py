import pytest
from apps.tenants.models.tenant import Tenant
from apps.authentication.models import User

@pytest.mark.django_db
class TestDomainResolution:
    def setup_method(self):
        # Create a dummy user for the owner field required by Tenant
        self.user = User.objects.create_user(email="owner@acme.com", password="password")
        self.tenant = Tenant.objects.create(
            tenant_name="Acme Corp", 
            company_name="Acme Corp", 
            tenant_code="acme",
            company_domain="www.acmecorp.com",
            owner=self.user
        )

    def test_subdomain_resolution(self):
        tenant = Tenant.objects.get(tenant_code="acme")
        assert tenant.tenant_name == "Acme Corp"

    def test_custom_domain_resolution(self):
        tenant = Tenant.objects.get(company_domain="www.acmecorp.com")
        assert tenant.id == self.tenant.id
