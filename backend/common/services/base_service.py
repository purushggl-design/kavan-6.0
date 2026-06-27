"""
KAVAN v6.0 — Base Service
============================================================
The Service layer contains all business logic.
Services are injected with repositories via dependency injection.

Rules:
  1. Services contain business logic — not views, not models
  2. Services call repositories for data access
  3. Services raise KavanBaseException subclasses on errors
  4. Services are stateless — no instance state between calls
  5. Services are unit-testable with mocked repositories

Usage:
    class UserService(BaseService):
        def __init__(self):
            super().__init__(UserRepository())

        def get_user(self, user_id: UUID) -> User:
            return self.repository.get_by_id(user_id)

        def create_user(self, email: str, password: str) -> User:
            # Business rules here
            if self.repository.exists(email=email):
                raise DuplicateValueException("Email already registered.")
            hashed = hash_password(password)
            return self.repository.create(email=email, password=hashed)
"""

import logging
from typing import Any, Optional

from common.repositories.base_repository import BaseRepository

logger = logging.getLogger("kavan")


class BaseService:
    """
    Abstract base service with dependency-injected repository.

    Subclass and inject the appropriate repository.
    Add domain-specific methods following SRP.
    """

    def __init__(self, repository: Optional[BaseRepository] = None):
        self.repository = repository
        self._logger = logging.getLogger(
            f"kavan.services.{self.__class__.__name__}"
        )

    def _log_operation(self, operation: str, **kwargs) -> None:
        """Log a service operation with context."""
        self._logger.info(
            f"{self.__class__.__name__}.{operation}",
            extra={"kavan_data": kwargs},
        )

    def _log_error(self, operation: str, error: Exception, **kwargs) -> None:
        """Log a service error with context."""
        self._logger.error(
            f"{self.__class__.__name__}.{operation} failed: {error}",
            extra={"kavan_data": kwargs},
            exc_info=True,
        )

    def execute(self, *args, **kwargs) -> Any:
        """
        Template method — override in subclasses for simple single-operation services.
        """
        raise NotImplementedError(
            f"{self.__class__.__name__} must implement execute()."
        )
