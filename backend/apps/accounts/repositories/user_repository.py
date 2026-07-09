from common.repositories.base_repository import BaseRepository
from apps.authentication.models import User

class UserRepository(BaseRepository):
    model = User

    def get_user_by_email(self, email: str) -> User:
        return self.get(email=email)
