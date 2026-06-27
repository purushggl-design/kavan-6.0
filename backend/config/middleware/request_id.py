"""
KAVAN v6.0 — Request ID Middleware
============================================================
Generates a unique UUID4 identifier for every HTTP request.

Features:
  - Reads existing X-Request-ID from incoming headers (proxy/LB support)
  - Generates a new UUID4 if not provided
  - Stores in thread-local storage for logger access
  - Injects X-Request-ID into every HTTP response

Thread-local access:
    from config.middleware.request_id import get_current_request_id
    request_id = get_current_request_id()
"""

import threading
import uuid

# Thread-local storage for cross-middleware / logger access
_request_id_local = threading.local()


def get_current_request_id() -> str:
    """Return the request ID for the current thread, or empty string."""
    return getattr(_request_id_local, "request_id", "")


def set_current_request_id(request_id: str) -> None:
    """Set the request ID for the current thread."""
    _request_id_local.request_id = request_id


def clear_current_request_id() -> None:
    """Clear the request ID from thread-local storage."""
    if hasattr(_request_id_local, "request_id"):
        del _request_id_local.request_id


def get_current_correlation_id() -> str:
    """Return the correlation ID for the current thread, or empty string."""
    return getattr(_request_id_local, "correlation_id", "")


def set_current_correlation_id(correlation_id: str) -> None:
    """Set the correlation ID for the current thread."""
    _request_id_local.correlation_id = correlation_id


def clear_current_correlation_id() -> None:
    """Clear the correlation ID from thread-local storage."""
    if hasattr(_request_id_local, "correlation_id"):
        del _request_id_local.correlation_id



class RequestIDMiddleware:
    """
    Middleware that assigns a unique request ID to every HTTP request.

    Priority:
        1. X-Request-ID header from client/proxy
        2. Generated UUID4

    The request ID is:
        - Stored in request.request_id
        - Stored in thread-local for logger access
        - Returned in X-Request-ID response header
    """

    HEADER_NAME = "HTTP_X_REQUEST_ID"
    RESPONSE_HEADER = "X-Request-ID"

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Extract or generate request ID
        request_id = (
            request.META.get(self.HEADER_NAME)
            or str(uuid.uuid4())
        )

        # Attach to request object
        request.request_id = request_id

        # Store in thread-local for logger access
        set_current_request_id(request_id)

        try:
            response = self.get_response(request)
        finally:
            # Always clean up thread-local to avoid leaks
            clear_current_request_id()

        # Inject into response headers
        response[self.RESPONSE_HEADER] = request_id

        return response
