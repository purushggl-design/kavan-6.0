"""
KAVAN v6.0 — Service Interface
============================================================
Defines the abstract base class for services.
"""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Any

T_in = TypeVar("T_in")
T_out = TypeVar("T_out")

class IService(ABC, Generic[T_in, T_out]):
    """
    Abstract interface representing a business or infrastructure process service.
    """

    @abstractmethod
    def execute(self, request_data: T_in) -> T_out:
        """
        Runs the service operational logic.
        """
        pass
