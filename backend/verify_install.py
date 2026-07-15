import os
import django
import time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from apps.authentication.models import User
from apps.marketplace.models.application import Application, ApplicationVersion, TenantInstallation
from apps.tenants.models.tenant import Tenant
import docker
from config.celery import app as celery_app

# Force Celery to be completely synchronous for tests
celery_app.conf.task_always_eager = True
celery_app.conf.task_eager_propagates = True

def verify():
    print("Setting up install verification...")
    # Get or create tenant and user
    owner_user, _ = User.objects.get_or_create(username="tenant_owner", defaults={"email": "owner@test.com", "platform_role": None})
    tenant_c, _ = Tenant.objects.get_or_create(tenant_code="tenant_c", defaults={"tenant_name": "Tenant C", "owner": owner_user, "company_domain": "c.com"})
    user_c, _ = User.objects.get_or_create(username="user_c", defaults={"email": "userc@test.com", "tenant_id": tenant_c.id, "platform_role": None})

    # Setup application
    app, _ = Application.objects.get_or_create(
        code="test-web",
        defaults={
            "name": "Test Web Server",
            "description": "Minimal web server for testing provisioning."
        }
    )
    
    version, _ = ApplicationVersion.objects.get_or_create(
        application=app,
        version_number="1.0.0",
        defaults={
            "image_ref": "nginx:alpine",
            "manifest": {
                "env_schema": {"kavan_generated": ["SECRET_KEY"], "kavan_provisioned": ["DB_URL"]},
                "resources": {"mem_limit": "256m"},
                "runtime": {"container_port": 80, "health_check_path": "/"}
            },
            "is_active": True
        }
    )

    # Clean any existing installations for this test
    TenantInstallation.objects.filter(tenant=tenant_c, version=version).delete()

    from django.test import Client
    client = Client()
    client.force_login(user_c)

    print("POST /api/v1/marketplace/install/{version_id}/...")
    res = client.post(f'/api/v1/marketplace/install/{version.id}/')
    assert res.status_code == 202, f"Expected 202, got {res.status_code}: {res.content}"
    
    data = res.json()
    installation_id = data.get('installation_id')
    assert installation_id, "Missing installation_id in response"
    
    print(f"Installation created: {installation_id}. Waiting for celery task to complete...")
    
    # Wait for celery to process
    status = 'PENDING'
    for _ in range(30):
        installation = TenantInstallation.objects.get(id=installation_id)
        status = installation.status
        if status in ['RUNNING', 'FAILED']:
            break
        time.sleep(1)
        
    print(f"Final DB Status: {status}")
    assert status == 'RUNNING', f"Installation failed or timed out. Status: {status}"
    
    print("Connecting to local Docker daemon to verify container...")
    dclient = docker.from_env()
    container_name = f"kavan_tenant_tenant_c_test-web"
    
    try:
        container = dclient.containers.get(container_name)
        print(f"SUCCESS! Container found: {container.name} (Status: {container.status})")
        print("Traefik Routing Labels Generated:")
        for k, v in container.labels.items():
            if 'traefik' in k:
                print(f"  {k}: {v}")
    except docker.errors.NotFound:
        assert False, f"Container {container_name} not found in Docker!"

if __name__ == '__main__':
    verify()
