from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.marketplace.models.product import TenantProduct
from apps.deployments.models import DeploymentTemplate
from apps.deployments.services.deployment_service import DeploymentService
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=TenantProduct)
def trigger_deployment(sender, instance, created, **kwargs):
    """
    Signals: When a TenantProduct is created, trigger a Deployment Request automatically.
    """
    if created and not instance.is_installed:
        # Find default template for product
        template = DeploymentTemplate.objects.filter(product=instance.product).first()
        if template:
            logger.info(f"Signal triggered: Queuing deployment for Tenant {instance.tenant.name}, Product {instance.product.name}")
            deployment = DeploymentService.request_deployment(
                tenant=instance.tenant,
                product=instance.product,
                tenant_product=instance,
                template=template
            )
            
            # Update the Marketplace TenantProduct marker
            instance.deployment_id = str(deployment.id)
            instance.deployment_status = 'REQUESTED'
            instance.save(update_fields=['deployment_id', 'deployment_status'])
        else:
            logger.warning(f"No DeploymentTemplate found for Product {instance.product.name}. Skipping auto-deployment.")
