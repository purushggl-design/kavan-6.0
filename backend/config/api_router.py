"""
KAVAN v6.0 — API Router (v1)
============================================================
Centralised DRF router for API version 1.
Future layers register their ViewSets here.

Usage:
    # In apps/authentication/urls.py:
    from config.api_router import router
    router.register(r"auth", AuthViewSet, basename="auth")
"""

from django.urls import path
from rest_framework.routers import DefaultRouter

# Create the v1 router
router = DefaultRouter()

# ============================================================
# LAYER 2+ — Register ViewSets below as layers are built
# ============================================================

# Layer 2 — Authentication
# router.register(r"auth", AuthViewSet, basename="auth")
# router.register(r"users", UserViewSet, basename="users")

# Layer 3 — Tenants
# router.register(r"tenants", TenantViewSet, basename="tenants")

# Layer 4 — RBAC
# router.register(r"roles", RoleViewSet, basename="roles")
# router.register(r"permissions", PermissionViewSet, basename="permissions")

# Layer 5 — Products / Marketplace
from apps.marketplace.api.platform_views import PlatformProductViewSet
from apps.marketplace.api.tenant_views import TenantMarketplaceViewSet

router.register(r"platform/products", PlatformProductViewSet, basename="platform-products")
router.register(r"marketplace", TenantMarketplaceViewSet, basename="tenant-marketplace")
# Export the URL patterns for inclusion in urls.py
app_name = "api_v1"
urlpatterns = router.urls
