from typing import List, Dict, Any
from apps.accounts.repositories.user_repository import UserRepository
from config.exceptions.business import ResourceNotFoundException

class AccountService:
    def __init__(self):
        self.user_repo = UserRepository()
        
    def list_users(self, **filters) -> List[Any]:
        return self.user_repo.filter(**filters)
        
    def get_user(self, user_id: str) -> Any:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise ResourceNotFoundException("User")
        return user
        
    def update_user(self, user_id: str, data: Dict[str, Any]) -> Any:
        user = self.get_user(user_id)
        return self.user_repo.update(user, **data)
        
    def delete_user(self, user_id: str) -> None:
        user = self.get_user(user_id)
        self.user_repo.delete(user)
