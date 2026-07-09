from common.repositories.base_repository import BaseRepository
from apps.profiles.models import UserProfile

class ProfileRepository(BaseRepository):
    model = UserProfile
    
    def get_by_user_id(self, user_id: str) -> UserProfile:
        return self.get(user_id=user_id)
