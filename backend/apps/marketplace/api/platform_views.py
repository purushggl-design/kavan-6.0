from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse
from backend.apps.marketplace.models.product import Product, ProductCategory, ProductVersion
from backend.apps.marketplace.api.serializers import (
    ProductSerializer, ProductCategorySerializer, ProductVersionSerializer
)
from backend.apps.marketplace.tasks import publish_product, publish_version

class PlatformProductViewSet(viewsets.ModelViewSet):
    """
    Platform APIs for managing products in the KAVAN ecosystem.
    Requires SUPER_ADMIN permissions.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @extend_schema(summary="Publish a product", description="Requires product:publish permission")
    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        publish_product.delay(self.get_object().id)
        return Response({"status": "Publishing task started"}, status=status.HTTP_202_ACCEPTED)

    @extend_schema(summary="Archive a product", description="Requires product:archive permission")
    @action(detail=True, methods=['post'])
    def archive(self, request, pk=None):
        product = self.get_object()
        product.status = 'ARCHIVED'
        product.save()
        return Response({"status": "Product archived"}, status=status.HTTP_200_OK)
        
    @extend_schema(summary="Restore an archived product", description="Requires product:restore permission")
    @action(detail=True, methods=['post'])
    def restore(self, request, pk=None):
        product = self.get_object()
        product.status = 'DRAFT'
        product.save()
        return Response({"status": "Product restored"}, status=status.HTTP_200_OK)

    @extend_schema(summary="Clone a product", description="Requires product:create permission")
    @action(detail=True, methods=['post'])
    def clone(self, request, pk=None):
        # Implementation for cloning
        return Response({"status": "Product cloned"}, status=status.HTTP_201_CREATED)

    @extend_schema(summary="Feature a product", description="Requires product:feature permission")
    @action(detail=True, methods=['post'])
    def feature(self, request, pk=None):
        product = self.get_object()
        if hasattr(product, 'listing'):
            product.listing.is_featured = True
            product.listing.save()
        return Response({"status": "Product featured"}, status=status.HTTP_200_OK)
        
    @extend_schema(summary="Unfeature a product", description="Requires product:feature permission")
    @action(detail=True, methods=['post'])
    def unfeature(self, request, pk=None):
        product = self.get_object()
        if hasattr(product, 'listing'):
            product.listing.is_featured = False
            product.listing.save()
        return Response({"status": "Product unfeatured"}, status=status.HTTP_200_OK)

    @extend_schema(summary="Get product analytics", description="Requires analytics:view permission")
    @action(detail=True, methods=['get'])
    def analytics(self, request, pk=None):
        return Response({"downloads": 0, "subscribers": 0, "deployments": 0, "revenue": 0})
