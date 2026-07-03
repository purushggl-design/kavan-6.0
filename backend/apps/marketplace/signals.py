from django.db.models.signals import post_save
from django.dispatch import receiver
from .models.product import Product, MarketplaceListing, ProductVersion
# from apps.audit.services.audit_service import AuditService
# Assuming AnalyticsService will be implemented
# from .services.analytics_service import AnalyticsService

@receiver(post_save, sender=Product)
def product_post_save(sender, instance, created, **kwargs):
    if created:
        # Automatically create a marketplace listing
        MarketplaceListing.objects.create(product=instance)
        
        # Create a default draft version
        ProductVersion.objects.create(
            product=instance,
            version_number="0.1.0-draft",
            release_notes="Initial Draft",
            status="DRAFT"
        )
        
        # Log to Audit (Disabled until AuditService is implemented)
        # try:
        #     AuditService.log_event(
        #         action="PRODUCT_CREATED",
        #         resource_type="Product",
        #         resource_id=str(instance.id),
        #         details={"product_name": instance.name, "product_code": instance.code}
        #     )
        # except Exception:
        #     pass # Suppress if Audit is not fully configured yet
        
        # Create analytics record
        # AnalyticsService.create_initial_record(instance.id)
