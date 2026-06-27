"""
KAVAN v6.0 — JSON Logger Wrapper
"""

import logging
from typing import Any, Optional

from config.middleware.request_id import get_current_request_id


class KavanLogger:
    """
    Wrapper around Python's standard logger that automatically
    injects request_id and formats extra data.

    Usage:
        from common.logging.json_logger import KavanLogger
        logger = KavanLogger(__name__)
        logger.info("User logged in", user_id="abc123", action="login")
    """

    def __init__(self, name: str):
        self._logger = logging.getLogger(name)

    def _log(self, level: str, message: str, **kwargs) -> None:
        """Internal log dispatcher."""
        extra = {
            "kavan_data": {
                "request_id": get_current_request_id(),
                **kwargs,
            }
        }
        getattr(self._logger, level)(message, extra=extra)

    def debug(self, message: str, **kwargs) -> None:
        self._log("debug", message, **kwargs)

    def info(self, message: str, **kwargs) -> None:
        self._log("info", message, **kwargs)

    def warning(self, message: str, **kwargs) -> None:
        self._log("warning", message, **kwargs)

    def error(self, message: str, exc_info: bool = False, **kwargs) -> None:
        extra = {"kavan_data": {"request_id": get_current_request_id(), **kwargs}}
        self._logger.error(message, extra=extra, exc_info=exc_info)

    def critical(self, message: str, **kwargs) -> None:
        self._log("critical", message, **kwargs)

    def audit(self, action: str, resource: str, resource_id: Optional[str] = None, **kwargs) -> None:
        """Log an audit event to the audit logger."""
        audit_logger = logging.getLogger("kavan.audit")
        audit_logger.info(
            f"AUDIT: {action} on {resource}",
            extra={
                "kavan_data": {
                    "action": action,
                    "resource": resource,
                    "resource_id": resource_id,
                    "request_id": get_current_request_id(),
                    **kwargs,
                }
            },
        )

    def security(self, event: str, **kwargs) -> None:
        """Log a security event to the security logger."""
        security_logger = logging.getLogger("kavan.security")
        security_logger.warning(
            f"SECURITY: {event}",
            extra={
                "kavan_data": {
                    "security_event": event,
                    "request_id": get_current_request_id(),
                    **kwargs,
                }
            },
        )
