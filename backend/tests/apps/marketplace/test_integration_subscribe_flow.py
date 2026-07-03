import pytest
from apps.marketplace.models.product import Product, ProductVersion, TenantProduct
from apps.tenants.models.tenant import Tenant
from apps.authentication.models import User

@pytest.mark.django_db
class TestIntegrationSubscribeFlow:
    def test_marketplace_subscribe_flow(self):
        # 1. Tenant Creation
        owner = User.objects.create_user(email="owner_market@example.com", password="password")
        tenant = Tenant.objects.create(
            tenant_code="MKTP",
            tenant_name="Marketplace Corp",
            company_name="Marketplace Corp",
            company_domain="mktp.example.com",
            owner=owner
        )

        # 2. Create Product
        product = Product.objects.create(
            code="erp",
            name="Enterprise ERP",
            slug="enterprise-erp",
            status="PUBLISHED",
            visibility="PUBLIC"
        )
        assert Product.objects.count() == 1

        # 3. Publish Version
        version = ProductVersion.objects.create(
            product=product,
            version_number="1.0.0",
            is_stable=True,
            is_latest=True
        )
        assert version.version_number == "1.0.0"

        # 4. Tenant Subscribes
        tenant_product = TenantProduct.objects.create(
            tenant=tenant,
            product=product,
            version=version,
            status='ACTIVE'
        )
        assert TenantProduct.objects.filter(tenant=tenant, product=product, status='ACTIVE').exists()

        # 5. Tenant Unsubscribes
        tenant_product.status = 'EXPIRED'
        tenant_product.save()
        
        assert TenantProduct.objects.filter(tenant=tenant, product=product, status='EXPIRED').exists()
