"""
KAVAN v6.0 — Unified Request Context
============================================================
Thread-local request context storing request identifiers and client details.
"""

import threading
from typing import Any, Dict, Optional

_context_local = threading.local()

class RequestContext:
    """
    A class to hold request-scoped variables (e.g., request_id, correlation_id,
    user_id, tenant_id, client_ip) so they can be easily retrieved anywhere
    in the execution flow (e.g., repository layer, celery tasks).
    """

    def __init__(
        self,
        request_id: str = "",
        correlation_id: str = "",
        user_id: Optional[Any] = None,
        tenant_id: Optional[Any] = None,
        client_ip: Optional[str] = None,
    ):
        self.request_id = request_id
        self.correlation_id = correlation_id
        self.user_id = user_id
        self.tenant_id = tenant_id
        self.client_ip = client_ip

    def to_dict(self) -> Dict[str, Any]:
        """Convert context values to a dictionary."""
        return {
            "request_id": self.request_id,
            "correlation_id": self.correlation_id,
            "user_id": self.user_id,
            "tenant_id": self.tenant_id,
            "client_ip": self.client_ip,
        }


def get_request_context() -> RequestContext:
    """Get the RequestContext of the current thread."""
    if not hasattr(_context_local, "context"):
        _context_local.context = RequestContext()
    return _context_local.context


def set_request_context(context: RequestContext) -> None:
    """Set the RequestContext of the current thread."""
    _context_local.context = context


def clear_request_context() -> None:
    """Clear the RequestContext of the current thread."""
    if hasattr(_context_local, "context"):
        del _context_local.context
