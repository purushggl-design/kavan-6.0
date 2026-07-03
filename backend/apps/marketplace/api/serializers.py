from rest_framework import serializers
from apps.marketplace.models.product import (
    Product, ProductVersion, ProductCategory, ProductDependency,
    MarketplaceListing, TenantProduct
)

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = '__all__'

class ProductVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVersion
        fields = '__all__'
        
class ProductDependencySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDependency
        fields = '__all__'

class MarketplaceListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketplaceListing
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category_details = ProductCategorySerializer(source='category', read_only=True)
    listing = MarketplaceListingSerializer(read_only=True)
    versions = ProductVersionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Product
        fields = '__all__'

class TenantProductSerializer(serializers.ModelSerializer):
    product_details = ProductSerializer(source='product', read_only=True)
    version_details = ProductVersionSerializer(source='version', read_only=True)

    class Meta:
        model = TenantProduct
        fields = '__all__'
