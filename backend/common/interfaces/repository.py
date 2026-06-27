"""
KAVAN v6.0 — Repository Interface
============================================================
Defines the abstract base class for repositories, ensuring a
consistent CRUD interface.
"""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional, Any, Dict

T = TypeVar("T")

class IRepository(ABC, Generic[T]):
    """
    Abstract interface for all domain/infrastructure repositories.
    """

    @abstractmethod
    def get_by_id(self, id: Any) -> Optional[T]:
        """Retrieve an entity by its identifier."""
        pass

    @abstractmethod
    def list(self, filters: Optional[Dict[str, Any]] = None) -> List[T]:
        """List entities matching optional filter criteria."""
        pass

    @abstractmethod
    def create(self, data: Dict[str, Any]) -> T:
        """Persist a new entity instance."""
        pass

    @abstractmethod
    def update(self, id: Any, data: Dict[str, Any]) -> Optional[T]:
        """Update an existing entity."""
        pass

    @abstractmethod
    def delete(self, id: Any) -> bool:
        """Remove an entity by its identifier."""
        pass
