from common.repositories.base_repository import BaseRepository
from apps.marketplace.models.product import ProductDependency

class DependencyRepository(BaseRepository):
    model = ProductDependency

    @classmethod
    def get_dependencies_for_product(cls, product_id):
        return cls.get_queryset().filter(product_id=product_id)
