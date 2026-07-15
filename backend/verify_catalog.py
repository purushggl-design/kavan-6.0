import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from apps.authentication.models import User
from apps.marketplace.models.application import Application, ApplicationVersion
from apps.tenants.models.tenant import Tenant
import json

def verify():
    # 1. Setup Test Data
    print("Setting up test catalog data...")
    app, _ = Application.objects.get_or_create(
        code="nginx-app",
        defaults={
            "name": "Nginx Web Server",
            "description": "A high performance web server."
        }
    )
    
    version, _ = ApplicationVersion.objects.get_or_create(
        application=app,
        version_number="1.0.0",
        defaults={
            "image_ref": "nginx:alpine",
            "manifest": {
                "env_schema": {"kavan_generated": [], "kavan_provisioned": []},
                "resources": {"mem_limit": "256m"},
                "runtime": {"container_port": 80, "health_check_path": "/"}
            },
            "is_active": True
        }
    )
    
    # Get or create an owner user first
    owner_user, _ = User.objects.get_or_create(username="tenant_owner", defaults={"email": "owner@test.com", "platform_role": None})

    tenant_a, _ = Tenant.objects.get_or_create(tenant_code="tenant_a", defaults={"tenant_name": "Tenant A", "owner": owner_user, "company_domain": "a.com"})
    tenant_b, _ = Tenant.objects.get_or_create(tenant_code="tenant_b", defaults={"tenant_name": "Tenant B", "owner": owner_user, "company_domain": "b.com"})
    
    user_a, _ = User.objects.get_or_create(username="user_a", defaults={"email": "usera@test.com", "tenant_id": tenant_a.id, "platform_role": None})
    user_b, _ = User.objects.get_or_create(username="user_b", defaults={"email": "userb@test.com", "tenant_id": tenant_b.id, "platform_role": None})

    from django.test import Client
    
    # 2. Test Tenant A
    print("Fetching catalog as Tenant A...")
    client_a = Client()
    client_a.force_login(user_a)
    res_a = client_a.get('/api/v1/marketplace/catalog/')
    
    # 3. Test Tenant B
    print("Fetching catalog as Tenant B...")
    client_b = Client()
    client_b.force_login(user_b)
    res_b = client_b.get('/api/v1/marketplace/catalog/')
    
    # 4. Assertions
    assert res_a.status_code == 200
    assert res_b.status_code == 200
    
    data_a = res_a.json()
    data_b = res_b.json()
    
    print(f"Tenant A Response: {json.dumps(data_a, indent=2)}")
    print(f"Tenant B Response: {json.dumps(data_b, indent=2)}")
    
    assert data_a['data'] == data_b['data'], "Data payload must be identical for both tenants."
    
    # Assuming paginated response or list
    results = data_a.get('data', [])
    
    assert len(results) > 0, "Catalog should not be empty."
    
    item = results[0]
    
    assert "image_ref" not in item, "SECURITY LEAK: image_ref exposed!"
    assert "manifest" not in item, "SECURITY LEAK: manifest exposed!"
    
    print("SUCCESS: Catalog is identical across tenants and leaks NO infrastructure data!")

if __name__ == '__main__':
    verify()
