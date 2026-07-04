from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.deployments.api.platform_views import PlatformDeploymentViewSet
from apps.deployments.api.tenant_views import TenantDeploymentViewSet

router = DefaultRouter()
router.register(r'platform/deployments', PlatformDeploymentViewSet, basename='platform-deployments')
router.register(r'tenant/deployments', TenantDeploymentViewSet, basename='tenant-deployments')

urlpatterns = [
    path('', include(router.urls)),
]
