from common.repositories.base_repository import BaseRepository
from apps.marketplace.models.product import ProductCategory

class CategoryRepository(BaseRepository):
    model = ProductCategory
