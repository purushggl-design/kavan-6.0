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
from apps.rbac.api.views import RBACViewSet

router.register(r"platform/products", PlatformProductViewSet, basename="platform-products")
router.register(r"marketplace", TenantMarketplaceViewSet, basename="tenant-marketplace")
router.register(r"rbac", RBACViewSet, basename="rbac")
# Duplicate registrations removed to prevent operationId collisions
from django.urls import include, path

# Platform Tenant Management (full CRUD + approve/suspend/create-admin)
from apps.tenants.api.platform_views import (
    PlatformTenantListView,
    PlatformTenantDetailView,
    PlatformTenantApproveView,
    PlatformTenantSuspendView,
    PlatformTenantCreateAdminView,
)

# Export the URL patterns for inclusion in urls.py
app_name = "api_v1"
urlpatterns = router.urls + [
    path("auth/", include("apps.authentication.urls", namespace="auth")),
    path("accounts/", include("apps.accounts.api.urls", namespace="accounts")),
    path("profiles/", include("apps.profiles.api.urls", namespace="profiles")),
    path("devices/", include("apps.devices.api.urls", namespace="devices")),
    path("audit/", include("apps.audit.api.urls", namespace="audit")),
    path("monitoring/", include("apps.monitoring.api.urls")),
    path("", include("apps.tenants.urls")),
    path("", include("apps.deployments.urls")),

    # SIEM — detection rules, correlation rules, stats
    path("", include("apps.siem.api.urls")),

    # Incidents — alerts and incidents lifecycle
    path("", include("apps.incidents.api.urls")),

    # Platform Tenant Management API (full CRUD)
    path("platform/tenants/", PlatformTenantListView.as_view(), name="platform-tenant-list"),
    path("platform/tenants/<uuid:pk>/", PlatformTenantDetailView.as_view(), name="platform-tenant-detail"),
    path("platform/tenants/<uuid:pk>/approve/", PlatformTenantApproveView.as_view(), name="platform-tenant-approve"),
    path("platform/tenants/<uuid:pk>/suspend/", PlatformTenantSuspendView.as_view(), name="platform-tenant-suspend"),
    path("platform/tenants/<uuid:pk>/create-admin/", PlatformTenantCreateAdminView.as_view(), name="platform-tenant-create-admin"),
]
