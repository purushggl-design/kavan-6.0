from backend.common.repositories.base_repository import BaseRepository
from backend.apps.marketplace.models.product import Product

class ProductRepository(BaseRepository):
    model = Product

    @classmethod
    def get_by_code(cls, code: str) -> Product:
        return cls.get_queryset().filter(code=code).first()

    @classmethod
    def get_published(cls):
        from backend.apps.marketplace.models.product import ProductStatus
        return cls.get_queryset().filter(status=ProductStatus.PUBLISHED)
