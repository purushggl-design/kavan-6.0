from backend.common.repositories.base_repository import BaseRepository
from backend.apps.marketplace.models.product import MarketplaceListing

class MarketplaceRepository(BaseRepository):
    model = MarketplaceListing

    @classmethod
    def get_featured(cls):
        return cls.get_queryset().filter(is_featured=True)

    @classmethod
    def get_trending(cls):
        return cls.get_queryset().filter(is_trending=True)
