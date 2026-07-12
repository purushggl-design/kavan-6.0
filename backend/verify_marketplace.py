import os
import django
import requests

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from apps.authentication.models import User
from apps.marketplace.models.application import Application

def verify():
    # 1. Setup Data
    print("Setting up test Application...")
    app, created = Application.objects.get_or_create(
        code="test-app-1",
        defaults={
            "name": "Test Application",
            "description": "An app for testing."
        }
    )
    print(f"Application ID: {app.id}")

    # Get a token for SuperAdmin
    superadmin = User.objects.filter(platform_role='SUPER_ADMIN').first()
    if not superadmin:
        print("No super admin found.")
        return

    # In development, we can just use simple JWT auth if implemented, or we can use the backend DB to bypass login for the test if it's too hard.
    # Actually, we can just use the requests library if we have a token, but let's just use the Django test client to bypass network issues.
    
    from django.test import Client
    client = Client()
    client.force_login(superadmin)

    # 2. Test Invalid Manifest
    print("Testing INVALID manifest (missing health_check_path)...")
    invalid_payload = {
        "application": app.id,
        "version_number": "1.0.0",
        "image_ref": "localhost:5000/test-app:1.0.0",
        "manifest": {
            "env_schema": {},
            "resources": {},
            "runtime": {
                "container_port": 8080
            }
        }
    }
    
    response = client.post('/api/v1/marketplace/versions/', data=invalid_payload, content_type='application/json')
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.content}")
    assert response.status_code == 400, "Should reject invalid manifest"
    print("Invalid manifest successfully rejected!")

    # 3. Test Valid Manifest
    print("Testing VALID manifest...")
    valid_payload = {
        "application": app.id,
        "version_number": "1.0.0",
        "image_ref": "localhost:5000/test-app:1.0.0",
        "manifest": {
            "env_schema": {},
            "resources": {},
            "runtime": {
                "container_port": 8080,
                "health_check_path": "/health"
            }
        }
    }
    
    response = client.post('/api/v1/marketplace/versions/', data=valid_payload, content_type='application/json')
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.content}")
    assert response.status_code == 201, "Should accept valid manifest"
    print("Valid manifest successfully accepted and saved!")

if __name__ == '__main__':
    verify()
