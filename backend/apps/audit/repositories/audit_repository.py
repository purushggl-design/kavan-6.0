from common.repositories.base_repository import BaseRepository
from apps.audit.models import AuditEvent

class AuditRepository(BaseRepository):
    model = AuditEvent
    
    def get_events_for_user(self, user_id: str):
        return self.filter(user_id=user_id)
