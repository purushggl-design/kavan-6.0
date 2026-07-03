from apps.marketplace.repositories.product_repository import ProductRepository
from apps.marketplace.models.product import ProductStatus

class ProductService:
    def __init__(self):
        self.product_repo = ProductRepository()

    def create_product(self, data: dict):
        return self.product_repo.create(**data)
        
    def update_product(self, product_id: str, data: dict):
        product = self.product_repo.get_by_id(product_id)
        if product:
            return self.product_repo.update(product, **data)
        return None
        
    def publish_product(self, product_id: str):
        product = self.product_repo.get_by_id(product_id)
        if product:
            return self.product_repo.update(product, status=ProductStatus.PUBLISHED)
        return None
