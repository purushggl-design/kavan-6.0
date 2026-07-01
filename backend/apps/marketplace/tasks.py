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
    # Example logic: update popularity based on downloads
    listings = MarketplaceListing.objects.all()
    for listing in listings:
        if listing.downloads > 1000:
            listing.is_popular = True
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
    return True

@shared_task
def update_product_statistics():
    logger.info("Updating product statistics...")
    return True

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
