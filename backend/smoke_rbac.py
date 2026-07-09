import os, django
os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings.development"
django.setup()

from rest_framework.test import APIRequestFactory, force_authenticate
from django.contrib.auth import get_user_model
from apps.marketplace.api.platform_views import PlatformProductViewSet

User = get_user_model()
factory = APIRequestFactory()

# Test 1: Anonymous user -> must get 403
print("=== Test 1: Anonymous user (no auth) ===")
request = factory.get("/api/v1/platform/products/")
view = PlatformProductViewSet.as_view({"get": "list"})
response = view(request)
print(f"  Status: {response.status_code} (expected 403)")

# Test 2: Regular user (no platform_role) -> must get 403
print("=== Test 2: Regular user (no platform role) ===")
User.objects.filter(email="rbactest_regular@test.com").delete()
regular_user = User.objects.create_user(email="rbactest_regular@test.com", password="test", platform_role="")
request2 = factory.get("/api/v1/platform/products/")
force_authenticate(request2, user=regular_user)
response2 = view(request2)
print(f"  Status: {response2.status_code} (expected 403)")

# Test 3: SUPER_ADMIN user -> must get 200
print("=== Test 3: SUPER_ADMIN user ===")
User.objects.filter(email="rbactest_admin@test.com").delete()
admin_user = User.objects.create_user(email="rbactest_admin@test.com", password="test", platform_role="SUPER_ADMIN")
request3 = factory.get("/api/v1/platform/products/")
force_authenticate(request3, user=admin_user)
response3 = view(request3)
print(f"  Status: {response3.status_code} (expected 200)")

regular_user.delete()
admin_user.delete()
print("DONE")
