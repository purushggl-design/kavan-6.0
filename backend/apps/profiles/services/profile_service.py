from typing import Dict, Any
from apps.profiles.repositories.profile_repository import ProfileRepository
from config.exceptions.business import ResourceNotFoundException

class ProfileService:
    def __init__(self):
        self.repo = ProfileRepository()
        
    def get_my_profile(self, user_id: str) -> Any:
        profile = self.repo.get_by_user_id(user_id)
        if not profile:
            raise ResourceNotFoundException("Profile")
        return profile
        
    def update_my_profile(self, user_id: str, data: Dict[str, Any]) -> Any:
        profile = self.get_my_profile(user_id)
        return self.repo.update(profile, **data)
