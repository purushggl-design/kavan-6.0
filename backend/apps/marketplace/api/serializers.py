from rest_framework import serializers
from apps.marketplace.models.product import (
    Product, ProductVersion, ProductCategory, ProductDependency,
    MarketplaceListing, TenantProduct
)
from apps.marketplace.models.application import (
    Application, ApplicationVersion, TenantInstallation
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

class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'

class ApplicationVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationVersion
        fields = '__all__'

    def validate_manifest(self, value):
        from apps.marketplace.models.application import validate_manifest
        validate_manifest(value)
        return value

class TenantInstallationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantInstallation
        fields = '__all__'

class MarketplaceCatalogSerializer(serializers.ModelSerializer):
    """
    Public-facing catalog serializer.
    STRICTLY MUST NOT expose image_ref, manifest, or other infrastructure data.
    """
    application_name = serializers.CharField(source='application.name', read_only=True)
    application_code = serializers.CharField(source='application.code', read_only=True)
    application_description = serializers.CharField(source='application.description', read_only=True)
    
    class Meta:
        model = ApplicationVersion
        fields = (
            'id', 
            'version_number', 
            'application_name', 
            'application_code', 
            'application_description'
        )

class TenantInstallationSafeSerializer(serializers.ModelSerializer):
    """
    Tenant-scoped installation serializer.
    STRICTLY MUST NOT expose container_id, container_name, or injected_env.
    """
    application_name = serializers.CharField(source='version.application.name', read_only=True)
    version_number = serializers.CharField(source='version.version_number', read_only=True)
    installed_at = serializers.DateTimeField(source='created_at', read_only=True)
    last_health_check = serializers.DateTimeField(source='updated_at', read_only=True)
    
    class Meta:
        model = TenantInstallation
        fields = (
            'id',
            'application_name',
            'version_number',
            'status',
            'route_path',
            'installed_at',
            'last_health_check'
        )
