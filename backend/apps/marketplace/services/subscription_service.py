from backend.apps.marketplace.repositories.tenant_product_repository import TenantProductRepository
from backend.apps.marketplace.repositories.product_repository import ProductRepository
import datetime

class SubscriptionService:
    def __init__(self):
        self.subscription_repo = TenantProductRepository()
        self.product_repo = ProductRepository()

    def subscribe_tenant(self, tenant_id: str, product_id: str, version_id: str = None):
        return self.subscription_repo.create(
            tenant_id=tenant_id,
            product_id=product_id,
            version_id=version_id,
            status='ACTIVE'
        )
        
    def install_product(self, subscription_id: str):
        subscription = self.subscription_repo.get_by_id(subscription_id)
        if subscription:
            # Layer 6 Trigger would happen here or in Celery Task
            return self.subscription_repo.update(subscription, is_installed=True)
        return None
