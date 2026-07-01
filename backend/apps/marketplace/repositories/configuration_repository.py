from backend.common.repositories.base_repository import BaseRepository
from backend.apps.marketplace.models.product import ProductConfiguration

class ConfigurationRepository(BaseRepository):
    model = ProductConfiguration

    @classmethod
    def get_configuration_for_product(cls, product_id):
        return cls.get_queryset().filter(product_id=product_id).first()
