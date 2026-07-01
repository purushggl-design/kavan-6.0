from backend.apps.marketplace.repositories.marketplace_repository import MarketplaceRepository
from backend.apps.marketplace.repositories.product_repository import ProductRepository

class MarketplaceService:
    def __init__(self):
        self.marketplace_repo = MarketplaceRepository()
        self.product_repo = ProductRepository()

    def get_published_products(self):
        return self.product_repo.get_published()
        
    def get_featured_products(self):
        return self.marketplace_repo.get_featured()
