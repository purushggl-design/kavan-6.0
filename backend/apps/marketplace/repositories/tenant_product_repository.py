from common.repositories.base_repository import BaseRepository
from apps.marketplace.models.product import TenantProduct

class TenantProductRepository(BaseRepository):
    model = TenantProduct

    @classmethod
    def get_subscriptions_for_tenant(cls, tenant_id):
        return cls.get_queryset().filter(tenant_id=tenant_id)
