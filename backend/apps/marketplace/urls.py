from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api.platform_views import PlatformProductViewSet
from .api.tenant_views import TenantMarketplaceViewSet

platform_router = DefaultRouter()
platform_router.register(r'products', PlatformProductViewSet, basename='platform-products')

tenant_router = DefaultRouter()
tenant_router.register(r'', TenantMarketplaceViewSet, basename='marketplace')

urlpatterns = [
    path('platform/', include(platform_router.urls)),
    path('tenant/', include(tenant_router.urls)),
]
