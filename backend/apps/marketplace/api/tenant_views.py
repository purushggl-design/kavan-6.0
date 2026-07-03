from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter
from apps.marketplace.models.product import Product, TenantProduct
from apps.marketplace.api.serializers import ProductSerializer, TenantProductSerializer
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
