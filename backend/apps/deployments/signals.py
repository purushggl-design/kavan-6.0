from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.marketplace.models.product import TenantProduct
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=TenantProduct)
def trigger_deployment(sender, instance, created, **kwargs):
    """
    Signals: When a TenantProduct is created, do NOT auto-deploy.
    Deployment must always be an explicit action triggered via the API.
    """
    if created:
        logger.info(f"Signal triggered: TenantProduct created for Tenant {instance.tenant.name}, Product {instance.product.name}. Auto-deployment is disabled per architectural rules.")
