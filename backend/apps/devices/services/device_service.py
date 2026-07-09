from typing import List, Any
from apps.devices.repositories.device_repository import DeviceRepository
from config.exceptions.business import ResourceNotFoundException

class DeviceService:
    def __init__(self):
        self.repo = DeviceRepository()
        
    def get_user_devices(self, user_id: str) -> List[Any]:
        return self.repo.get_user_devices(user_id=user_id)
        
    def delete_device(self, user_id: str, device_id: str) -> None:
        device = self.repo.get_by_id(device_id)
        if not device or str(device.user_id) != str(user_id):
            raise ResourceNotFoundException("Device")
        self.repo.delete(device)
