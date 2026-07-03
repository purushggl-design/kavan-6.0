from apps.marketplace.repositories.version_repository import VersionRepository

class VersionService:
    def __init__(self):
        self.version_repo = VersionRepository()

    def add_version(self, product_id: str, data: dict):
        data['product_id'] = product_id
        return self.version_repo.create(**data)
