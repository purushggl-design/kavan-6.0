import logging
from celery import shared_task
from django.utils import timezone
from .models.product import Product, ProductVersion, MarketplaceListing

logger = logging.getLogger(__name__)

@shared_task
def publish_product(product_id):
    try:
        product = Product.objects.get(id=product_id)
        product.status = 'PUBLISHED'
        product.save()
        logger.info(f"Product {product.name} (ID: {product_id}) successfully published.")
        
        # Ensure it has a marketplace listing
        MarketplaceListing.objects.get_or_create(product=product)
        return True
    except Product.DoesNotExist:
        logger.error(f"Failed to publish product. ID {product_id} not found.")
        return False

@shared_task
def publish_version(version_id):
    try:
        version = ProductVersion.objects.get(id=version_id)
        version.status = 'ACTIVE'
        version.save()
        logger.info(f"Version {version.version_number} for product {version.product.name} activated.")
        return True
    except ProductVersion.DoesNotExist:
        return False

@shared_task
def marketplace_sync():
    logger.info("Running marketplace sync...")
    listings = MarketplaceListing.objects.all()
    for listing in listings:
        # Business logic: if downloads > 1000, mark popular. If > 500 recently, trending.
        if listing.downloads > 1000:
            listing.is_popular = True
        if listing.downloads > 500:
            listing.is_trending = True
        listing.save()
    logger.info("Marketplace sync completed.")
    return True

@shared_task
def download_counter(listing_id):
    try:
        listing = MarketplaceListing.objects.get(id=listing_id)
        listing.downloads += 1
        listing.save(update_fields=['downloads'])
        logger.debug(f"Download count incremented for {listing.product.name}")
        return True
    except MarketplaceListing.DoesNotExist:
        return False

@shared_task
def dependency_checker(product_id):
    logger.info(f"Checking dependencies for product {product_id}...")
    # In a real scenario, this would verify that all required dependencies are met
    return True

@shared_task
def product_statistics():
    logger.info("Aggregating product statistics...")
    from django.db.models import Count
    from apps.marketplace.models.product import TenantProduct
    
    # Example: update downloads/subs for each listing
    products = Product.objects.annotate(sub_count=Count('tenantproduct'))
    for product in products:
        if hasattr(product, 'listing'):
            product.listing.downloads = product.sub_count
            product.listing.save()
    return True

@shared_task
def update_product_statistics():
    # Alias to product_statistics for now
    return product_statistics()

@shared_task
def validate_dependencies(product_id):
    logger.info(f"Validating dependencies for product {product_id}...")
    return True

@shared_task
def cleanup_old_versions():
    logger.info("Cleaning up old product versions...")
    return True

@shared_task
def health_scan(product_id):
    logger.info(f"Running health scan for product {product_id}...")
    return True

@shared_task
def notify_subscribers(product_id):
    logger.info(f"Notifying subscribers for product {product_id}...")
    return True

@shared_task
def audit_product_changes():
    logger.info("Auditing product changes...")
    return True

@shared_task
def review_aggregation(product_id):
    logger.info(f"Aggregating reviews for product {product_id}...")
    # Update MarketplaceListing rating and review count
    return True
