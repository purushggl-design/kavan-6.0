from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter
from apps.marketplace.models.product import Product, TenantProduct
from apps.marketplace.api.serializers import (
    ProductSerializer, TenantProductSerializer, MarketplaceCatalogSerializer,
    TenantInstallationSafeSerializer
)
from apps.marketplace.services.subscription_service import SubscriptionService

class TenantMarketplaceViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Tenant APIs for browsing the marketplace and managing subscriptions.
    """
    queryset = Product.objects.filter(status='PUBLISHED')
    serializer_class = ProductSerializer
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subscription_service = SubscriptionService()

    @extend_schema(summary="Search marketplace products", description="Requires marketplace:view permission")
    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('q', '')
        products = Product.objects.filter(name__icontains=query, status='PUBLISHED')
        return Response(ProductSerializer(products, many=True).data)

    @extend_schema(summary="Get trending products", description="Requires marketplace:view permission")
    @action(detail=False, methods=['get'])
    def trending(self, request):
        products = Product.objects.filter(status='PUBLISHED', listing__is_trending=True)
        return Response(ProductSerializer(products, many=True).data)

    @extend_schema(summary="Get featured products", description="Requires marketplace:view permission")
    @action(detail=False, methods=['get'])
    def featured(self, request):
        products = Product.objects.filter(status='PUBLISHED', listing__is_featured=True)
        return Response(ProductSerializer(products, many=True).data)

    @extend_schema(summary="Get latest products", description="Requires marketplace:view permission")
    @action(detail=False, methods=['get'])
    def latest(self, request):
        products = Product.objects.filter(status='PUBLISHED').order_by('-created_at')[:10]
        return Response(ProductSerializer(products, many=True).data)

    @extend_schema(summary="Subscribe to a product", description="Requires marketplace:subscribe permission")
    @action(detail=True, methods=['post'])
    def subscribe(self, request, pk=None):
        tenant_id = getattr(getattr(request, 'user', None), 'tenant_id', None)
        product = self.get_object()
        subscription = self.subscription_service.subscribe_tenant(tenant_id=tenant_id, product_id=product.id)
        return Response(TenantProductSerializer(subscription).data, status=status.HTTP_201_CREATED)

    @extend_schema(summary="Unsubscribe from a product", description="Requires marketplace:unsubscribe permission")
    @action(detail=True, methods=['delete'])
    def unsubscribe(self, request, pk=None):
        tenant_id = getattr(getattr(request, 'user', None), 'tenant_id', None)
        product = self.get_object()
        self.subscription_service.unsubscribe_tenant(tenant_id=tenant_id, product_id=product.id)
        return Response({"status": "Unsubscribed"}, status=status.HTTP_200_OK)

    @extend_schema(summary="Get active subscriptions", description="Requires marketplace:view permission")
    @action(detail=False, methods=['get'])
    def subscriptions(self, request):
        tenant_id = getattr(getattr(request, 'user', None), 'tenant_id', None)
        subs = TenantProduct.objects.filter(tenant_id=tenant_id, status='ACTIVE')
        return Response(TenantProductSerializer(subs, many=True).data)

    @extend_schema(summary="Get installed products", description="Requires product:view permission")
    @action(detail=False, methods=['get'])
    def installed(self, request):
        tenant_id = getattr(getattr(request, 'user', None), 'tenant_id', None)
        subs = TenantProduct.objects.filter(tenant_id=tenant_id, is_installed=True)
        return Response(TenantProductSerializer(subs, many=True).data)
        
    @extend_schema(summary="Request deployment (Layer 6)", description="Requires product:deploy permission")
    @action(detail=True, methods=['post'])
    def deploy(self, request, pk=None):
        # Trigger Layer 6
        return Response({"status": "Deployment requested"}, status=status.HTTP_202_ACCEPTED)

    @extend_schema(summary="Configure product", description="Requires product:configure permission")
    @action(detail=True, methods=['put'])
    def config(self, request, pk=None):
        return Response({"status": "Configuration updated"})

from rest_framework import generics
from apps.marketplace.models.application import ApplicationVersion, TenantInstallation
from apps.deployments.tasks import provision_tenant_service

class MarketplaceCatalogView(generics.ListAPIView):
    """
    GET /api/v1/marketplace/catalog/
    Public catalog for tenant users.
    """
    serializer_class = MarketplaceCatalogSerializer
    # No permission class required other than IsAuthenticated (default)
    
    def get_queryset(self):
        return ApplicationVersion.objects.filter(is_active=True)

class MarketplaceInstallView(generics.CreateAPIView):
    """
    POST /api/v1/marketplace/install/{version_id}/
    """
    def create(self, request, *args, **kwargs):
        version_id = self.kwargs.get('version_id')
        try:
            version = ApplicationVersion.objects.get(id=version_id, is_active=True)
        except ApplicationVersion.DoesNotExist:
            return Response({"error": "Version not found"}, status=status.HTTP_404_NOT_FOUND)
            
        tenant_id = getattr(request.user, 'tenant_id', None)
        if not tenant_id:
            return Response({"error": "No tenant associated with user"}, status=status.HTTP_400_BAD_REQUEST)
            
        from apps.tenants.models.tenant import Tenant
        try:
            tenant = Tenant.objects.get(id=tenant_id)
        except Tenant.DoesNotExist:
            return Response({"error": "Tenant does not exist"}, status=status.HTTP_400_BAD_REQUEST)
            
        # Check if already installed
        existing = TenantInstallation.objects.filter(tenant=tenant, version=version, status='RUNNING').first()
        if existing:
            return Response({"error": "Already installed"}, status=status.HTTP_400_BAD_REQUEST)
            
        # Create pending installation
        installation = TenantInstallation.objects.create(
            tenant=tenant,
            version=version,
            status='PENDING'
        )
        
        # Fire celery task
        provision_tenant_service.delay(installation.id)
        
        return Response({
            "status": "provisioning",
            "installation_id": installation.id
        }, status=status.HTTP_202_ACCEPTED)

from rest_framework.exceptions import NotFound

class TenantInstallationListView(generics.ListAPIView):
    """
    GET /api/v1/installations/
    """
    serializer_class = TenantInstallationSafeSerializer

    def get_queryset(self):
        tenant_id = getattr(self.request.user, 'tenant_id', None)
        if not tenant_id:
            return TenantInstallation.objects.none()
        return TenantInstallation.objects.filter(tenant_id=tenant_id)

class TenantInstallationDetailView(generics.RetrieveAPIView):
    """
    GET /api/v1/installations/{id}/
    """
    serializer_class = TenantInstallationSafeSerializer

    def get_object(self):
        tenant_id = getattr(self.request.user, 'tenant_id', None)
        if not tenant_id:
            raise NotFound()
            
        try:
            return TenantInstallation.objects.get(
                id=self.kwargs.get('pk'),
                tenant_id=tenant_id
            )
        except TenantInstallation.DoesNotExist:
            raise NotFound()
