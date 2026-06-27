"""
KAVAN v6.0 — Base Exception Classes
============================================================
All custom exceptions inherit from KavanBaseException.
This provides a consistent interface for exception handling
across the entire application.

Design principles:
  - Each exception carries HTTP status, error code, and message
  - Exception codes are human-readable (not numeric)
  - Details can carry arbitrary structured data
  - All exceptions are serializable to the standard error format
"""

from typing import Any, Dict, List, Optional


class KavanBaseException(Exception):
    """
    Base exception for all KAVAN application exceptions.

    Attributes:
        message:     User-facing error description
        code:        Machine-readable error code (e.g. "RESOURCE_NOT_FOUND")
        http_status: HTTP status code to return
        details:     Additional structured error data
    """

    http_status: int = 500
    code: str = "INTERNAL_ERROR"
    message: str = "An unexpected error occurred."

    def __init__(
        self,
        message: Optional[str] = None,
        code: Optional[str] = None,
        details: Optional[Any] = None,
        http_status: Optional[int] = None,
    ):
        self.message = message or self.__class__.message
        self.code = code or self.__class__.code
        self.details = details
        self.http_status = http_status or self.__class__.http_status
        super().__init__(self.message)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to the KAVAN error format."""
        error: Dict[str, Any] = {
            "code": self.code,
            "message": self.message,
        }
        if self.details is not None:
            error["details"] = self.details
        return error

    def to_error_list(self) -> List[Dict[str, Any]]:
        """Return as a list (for standard response format)."""
        return [self.to_dict()]

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"code={self.code!r}, "
            f"message={self.message!r}, "
            f"http_status={self.http_status})"
        )
