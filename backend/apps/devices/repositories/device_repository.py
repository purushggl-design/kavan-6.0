from common.repositories.base_repository import BaseRepository
from apps.devices.models import TrustedDevice

class DeviceRepository(BaseRepository):
    model = TrustedDevice
    
    def get_user_devices(self, user_id: str):
        return self.filter(user_id=user_id)
