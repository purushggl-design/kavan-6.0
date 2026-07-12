import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from apps.authentication.models import User
from apps.marketplace.models.application import Application, ApplicationVersion, TenantInstallation
from apps.tenants.models.tenant import Tenant
from django.test import Client

def verify():
    print("Setting up installations test data...")
    owner_user, _ = User.objects.get_or_create(username="tenant_owner", defaults={"email": "owner@test.com", "platform_role": "TENANT_ADMIN"})

    tenant_a, _ = Tenant.objects.get_or_create(tenant_code="tenant_a", defaults={"tenant_name": "Tenant A", "owner": owner_user, "company_domain": "a.com"})
    tenant_b, _ = Tenant.objects.get_or_create(tenant_code="tenant_b", defaults={"tenant_name": "Tenant B", "owner": owner_user, "company_domain": "b.com"})
    
    user_a, _ = User.objects.get_or_create(username="user_a", defaults={"email": "usera@test.com", "tenant_id": tenant_a.id, "platform_role": "TENANT_USER"})

    app, _ = Application.objects.get_or_create(code="test-app-1", defaults={"name": "Test Application", "description": "Test App"})
    version, _ = ApplicationVersion.objects.get_or_create(application=app, version_number="1.0.0", defaults={"image_ref": "test:latest", "manifest": {}, "is_active": True})

    # Clear old installations for isolation
    TenantInstallation.objects.filter(tenant__in=[tenant_a, tenant_b]).delete()

    # Create dummy installations
    install_a = TenantInstallation.objects.create(tenant=tenant_a, version=version, status="RUNNING", route_path="/t/tenant_a/test-app-1")
    install_b = TenantInstallation.objects.create(tenant=tenant_b, version=version, status="RUNNING", route_path="/t/tenant_b/test-app-1")

    client = Client()
    client.force_login(user_a)

    print("\n--- Test 1: Fetching Installations list for Tenant A ---")
    res_list = client.get('/api/v1/installations/')
    assert res_list.status_code == 200, f"Expected 200, got {res_list.status_code}"
    list_data = res_list.json()
    
    # Assert isolation
    data_array = list_data.get('data', [])
    print(f"List Response: {json.dumps(list_data, indent=2)}")
    
    assert len(data_array) == 1, f"Expected exactly 1 installation, got {len(data_array)}"
    assert data_array[0]['id'] == str(install_a.id), "Response must contain Tenant A's installation ID"
    assert str(install_b.id) not in json.dumps(list_data), "Tenant B's installation ID leaked in response!"

    print("\n--- Test 2: Attempting direct GET for Tenant B's installation as Tenant A ---")
    res_detail = client.get(f'/api/v1/installations/{install_b.id}/')
    print(f"Detail Response Status Code: {res_detail.status_code}")
    print(f"Detail Response: {res_detail.content.decode()}")
    
    # Must be 404, not 403 or 200
    assert res_detail.status_code == 404, f"Expected 404 Not Found, got {res_detail.status_code}"
    
    print("\nSUCCESS: Complete cross-tenant isolation verified (List filtered, Detail returns 404).")

if __name__ == '__main__':
    verify()
