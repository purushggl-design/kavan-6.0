from backend.common.repositories.base_repository import BaseRepository
from backend.apps.marketplace.models.product import ProductCategory

class CategoryRepository(BaseRepository):
    model = ProductCategory
