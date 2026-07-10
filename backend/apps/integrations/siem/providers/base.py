from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseSIEMProvider(ABC):
    """
    Abstract interface for all External SIEM providers.
    """
    
    @abstractmethod
    def forward(self, payload: Dict[str, Any]) -> bool:
        """
        Takes a normalized payload and forwards it to the SIEM.
        Should return True on success, False/raise Exception on failure.
        """
        pass
    
    @abstractmethod
    def normalize_event(self, event: Any) -> Dict[str, Any]:
        """
        Converts a KAVAN Event into the SIEM's preferred schema (e.g., Splunk CIM).
        """
        pass
