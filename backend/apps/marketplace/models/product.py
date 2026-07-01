from django.db import models
from backend.common.models.base_model import BaseModel
from backend.apps.tenants.models.tenant import Tenant

class ProductStatus(models.TextChoices):
    DRAFT = 'DRAFT', 'Draft'
    PUBLISHED = 'PUBLISHED', 'Published'
    ARCHIVED = 'ARCHIVED', 'Archived'

class ProductVisibility(models.TextChoices):
    PUBLIC = 'PUBLIC', 'Public'
    PRIVATE = 'PRIVATE', 'Private'
    TENANT_SPECIFIC = 'TENANT_SPECIFIC', 'Tenant Specific'

class ProductCategory(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        db_table = 'marketplace_categories'
        verbose_name_plural = 'Product Categories'

    def __str__(self):
        return self.name

class Product(BaseModel):
    code = models.CharField(max_length=100, unique=True, help_text='e.g., crm, erp')
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    short_description = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    vendor = models.CharField(max_length=255, blank=True)
    owner = models.CharField(max_length=255, blank=True) # Super Admin / Platform team
    status = models.CharField(max_length=32, choices=ProductStatus.choices, default=ProductStatus.DRAFT)
    visibility = models.CharField(max_length=32, choices=ProductVisibility.choices, default=ProductVisibility.PRIVATE)
    
    # Metadata
    logo = models.URLField(blank=True, max_length=1024)
    banner = models.URLField(blank=True, max_length=1024)
    icon = models.URLField(blank=True, max_length=1024)
    website = models.URLField(blank=True, max_length=1024)
    documentation_url = models.URLField(blank=True, max_length=1024)
    support_url = models.URLField(blank=True, max_length=1024)
    
    # License & Pricing
    license_type = models.CharField(max_length=100, blank=True)
    pricing_model = models.CharField(max_length=100, blank=True)
    
    class Meta:
        db_table = 'marketplace_products'

    def __str__(self):
        return self.name

class ProductVersion(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='versions')
    version_number = models.CharField(max_length=50, help_text='e.g., 1.2.0')
    release_date = models.DateTimeField(null=True, blank=True)
    release_notes = models.TextField(blank=True)
    
    # Platform Compatibility
    min_platform_version = models.CharField(max_length=50, blank=True)
    max_platform_version = models.CharField(max_length=50, blank=True)
    
    # Artifacts
    docker_image = models.CharField(max_length=255, blank=True)
    checksum = models.CharField(max_length=255, blank=True)
    download_url = models.URLField(blank=True, max_length=1024)
    size = models.BigIntegerField(null=True, blank=True, help_text="Size in bytes")
    
    # Flags
    is_stable = models.BooleanField(default=True)
    is_lts = models.BooleanField(default=False)
    is_latest = models.BooleanField(default=False)
    status = models.CharField(max_length=32, default='ACTIVE')

    class Meta:
        db_table = 'marketplace_product_versions'
        unique_together = ('product', 'version_number')

    def __str__(self):
        return f"{self.product.name} - {self.version_number}"

class ProductDependency(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='dependencies')
    depends_on = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='required_by')
    version_requirement = models.CharField(max_length=100, blank=True, help_text="e.g., >=1.0.0")
    is_required = models.BooleanField(default=True)

    class Meta:
        db_table = 'marketplace_product_dependencies'
        unique_together = ('product', 'depends_on')

class ProductConfiguration(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='configurations')
    environment_variables = models.JSONField(default=dict, blank=True)
    database_requirements = models.JSONField(default=dict, blank=True)
    redis_requirements = models.JSONField(default=dict, blank=True)
    memory_req = models.CharField(max_length=50, blank=True)
    cpu_req = models.CharField(max_length=50, blank=True)
    disk_req = models.CharField(max_length=50, blank=True)
    ports = models.JSONField(default=list, blank=True)

    class Meta:
        db_table = 'marketplace_product_configurations'

class MarketplaceListing(BaseModel):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='listing')
    is_featured = models.BooleanField(default=False)
    is_trending = models.BooleanField(default=False)
    is_popular = models.BooleanField(default=False)
    downloads = models.PositiveIntegerField(default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    reviews_count = models.PositiveIntegerField(default=0)
    
    class Meta:
        db_table = 'marketplace_listings'

class TenantProduct(BaseModel):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='subscriptions')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    version = models.ForeignKey(ProductVersion, on_delete=models.CASCADE, null=True, blank=True)
    
    subscription_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=32, default='ACTIVE') # ACTIVE, SUSPENDED, EXPIRED
    license_key = models.CharField(max_length=255, blank=True)
    expiry = models.DateTimeField(null=True, blank=True)
    auto_update = models.BooleanField(default=False)
    
    # Layer 6 will consume these fields
    is_installed = models.BooleanField(default=False)
    deployment_status = models.CharField(max_length=32, blank=True, help_text="Status for Layer 6 communication")
    deployment_id = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = 'marketplace_tenant_products'
        unique_together = ('tenant', 'product')
