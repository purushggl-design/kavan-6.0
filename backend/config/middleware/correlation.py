"""
KAVAN v6.0 — Correlation ID and Request Context Middleware
============================================================
Generates or propagates a Correlation-ID across systems.
Populates thread-local RequestContext.
"""

import uuid
from django.conf import settings
from config.middleware.request_id import (
    set_current_correlation_id,
    clear_current_correlation_id,
    get_current_request_id,
    get_current_correlation_id,
)
from config.feature_flags import ENABLE_CORRELATION_ID
from common.context.request_context import (
    RequestContext,
    set_request_context,
    clear_request_context,
)

class CorrelationIDMiddleware:
    """
    Middleware to propagate a Correlation ID from incoming headers
    or generate a new one if not provided.
    """

    HEADER_NAME = "HTTP_X_CORRELATION_ID"
    RESPONSE_HEADER = "X-Correlation-ID"

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not ENABLE_CORRELATION_ID:
            return self.get_response(request)

        # Extract or generate correlation ID
        correlation_id = (
            request.META.get(self.HEADER_NAME)
            or request.headers.get("x-correlation-id")
            or str(uuid.uuid4())
        )

        # Attach to request object
        request.correlation_id = correlation_id

        # Store in thread-local storage (defined in request_id.py)
        set_current_correlation_id(correlation_id)

        try:
            response = self.get_response(request)
        finally:
            # Clean up to avoid memory leaks
            clear_current_correlation_id()

        # Inject into response headers
        response[self.RESPONSE_HEADER] = correlation_id

        return response


class RequestContextMiddleware:
    """
    Middleware that populates the thread-local RequestContext
    with request details (IDs, client IP, authenticated user/tenant context).
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Extract client IP
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            client_ip = x_forwarded_for.split(",")[0].strip()
        else:
            client_ip = request.META.get("REMOTE_ADDR", "unknown")

        # Expose request/correlation IDs
        request_id = get_current_request_id() or getattr(request, "request_id", "")
        correlation_id = get_current_correlation_id() or getattr(request, "correlation_id", "")

        # Extract user & tenant if populated (populated by future layers)
        user_id = None
        user = getattr(request, "user", None)
        if user and hasattr(user, "id") and user.is_authenticated:
            user_id = user.id

        tenant_id = request.META.get("HTTP_X_TENANT_ID") or getattr(request, "tenant_id", None)

        # Create thread-local context
        context = RequestContext(
            request_id=request_id,
            correlation_id=correlation_id,
            user_id=user_id,
            tenant_id=tenant_id,
            client_ip=client_ip,
        )
        set_request_context(context)

        try:
            response = self.get_response(request)
        finally:
            # Clear to prevent cross-request leaks
            clear_request_context()

        return response
