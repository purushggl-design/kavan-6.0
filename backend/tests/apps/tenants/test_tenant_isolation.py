import pytest
from django.urls import reverse
from apps.tenants.models.tenant import Tenant

@pytest.mark.django_db
class TestTenantIsolation:
    def setup_method(self):
        from apps.authentication.models import User
        self.user = User.objects.create_user(email="owner_iso@example.com", password="password")
        self.tenant_a = Tenant.objects.create(tenant_code="tenant-a", tenant_name="Tenant A", company_name="Tenant A", company_domain="tenant-a.kavan.local", owner=self.user)
        self.tenant_b = Tenant.objects.create(tenant_code="tenant-b", tenant_name="Tenant B", company_name="Tenant B", company_domain="tenant-b.kavan.local", owner=self.user)

    def test_tenant_context_middleware(self, client):
        # Accessing tenant A should not expose tenant B data
        response = client.get('/', HTTP_HOST='tenant-a.kavan.local')
        # Middleware should attach tenant_a to request
        assert response.wsgi_request.tenant.id == self.tenant_a.id
        
    def test_tenant_scoped_manager(self):
        # Assuming we have a scoped model like TenantProduct
        # Tenant A should only see its own products
        pass

    def test_thread_local_cleanup(self):
        from apps.tenants.services.tenant_context_service import TenantContextService
        from apps.tenants.middleware.tenant_middleware import TenantMiddleware
        from django.test import RequestFactory
        
        factory = RequestFactory()
        middleware = TenantMiddleware(lambda req: None)
        
        # 1. Simulate a request matching Tenant A
        request_a = factory.get('/', HTTP_HOST='tenant-a.kavan.local')
        middleware.process_request(request_a)
        
        # Verify Tenant A is in ThreadLocal
        assert TenantContextService.get_current_tenant() == self.tenant_a
        
        # 2. Simulate Response, which should trigger cleanup
        middleware.process_response(request_a, None)
        assert TenantContextService.get_current_tenant() is None
        
        # 3. Simulate an Exception, which should also trigger cleanup
        middleware.process_request(request_a)
        assert TenantContextService.get_current_tenant() == self.tenant_a
        
        middleware.process_exception(request_a, Exception("Server Error"))
        assert TenantContextService.get_current_tenant() is None

    def test_thread_local_concurrency(self):
        from apps.tenants.services.tenant_context_service import TenantContextService
        import concurrent.futures
        import time
        
        def simulate_thread(tenant_mock):
            # Set tenant for this thread
            TenantContextService.set_current_tenant(tenant_mock)
            # Sleep to allow context switch and prove isolation
            time.sleep(0.1)
            # Retrieve it
            retrieved = TenantContextService.get_current_tenant()
            # Clean it
            TenantContextService.clear()
            return retrieved
            
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            future_a = executor.submit(simulate_thread, self.tenant_a)
            future_b = executor.submit(simulate_thread, self.tenant_b)
            
            tenant_for_a = future_a.result()
            tenant_for_b = future_b.result()
            
        assert tenant_for_a == self.tenant_a
        assert tenant_for_b == self.tenant_b
