from backend.common.repositories.base_repository import BaseRepository
from backend.apps.marketplace.models.product import ProductVersion

class VersionRepository(BaseRepository):
    model = ProductVersion
    
    @classmethod
    def get_versions_for_product(cls, product_id):
        return cls.get_queryset().filter(product_id=product_id)
