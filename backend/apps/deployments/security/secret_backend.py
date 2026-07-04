from abc import ABC, abstractmethod
from cryptography.fernet import Fernet
from django.conf import settings
import base64

class SecretBackend(ABC):
    @abstractmethod
    def encrypt(self, value: str) -> str:
        pass

    @abstractmethod
    def decrypt(self, encrypted_value: str) -> str:
        pass

class FernetSecretBackend(SecretBackend):
    def __init__(self):
        # Ensure 32 bytes URL-safe base64-encoded key
        key = settings.SECRET_KEY.encode()[:32].ljust(32, b'0')
        safe_key = base64.urlsafe_b64encode(key)
        self.cipher = Fernet(safe_key)

    def encrypt(self, value: str) -> str:
        if not value:
            return value
        return self.cipher.encrypt(value.encode()).decode()

    def decrypt(self, encrypted_value: str) -> str:
        if not encrypted_value:
            return encrypted_value
        return self.cipher.decrypt(encrypted_value.encode()).decode()

def get_secret_backend() -> SecretBackend:
    # Factory function for easy testing and dependency injection
    return FernetSecretBackend()
