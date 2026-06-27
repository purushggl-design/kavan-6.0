"""
KAVAN v6.0 — Global Exception Handler Middleware
============================================================
Catches all unhandled exceptions and formats them into
the KAVAN standard error response format.

This middleware complements DRF's built-in exception handler
(configured in REST_FRAMEWORK settings) by also catching
exceptions from non-DRF views, middleware, etc.

Response format:
{
    "success": false,
    "message": "...",
    "data": null,
    "errors": [...],
    "meta": {
        "timestamp": "...",
        "request_id": "...",
        "version": "v1"
    }
}
"""

import json
import logging
import traceback
from datetime import datetime, timezone

from django.http import JsonResponse

from config.middleware.request_id import get_current_request_id

logger = logging.getLogger("kavan.error")


class ExceptionHandlerMiddleware:
    """
    Global exception handler middleware.

    Catches unhandled exceptions and returns structured JSON error responses
    instead of Django's default HTML error pages.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
            return response
        except Exception as exc:
            return self._handle_exception(request, exc)

    def _handle_exception(self, request, exc: Exception) -> JsonResponse:
        """Convert an unhandled exception to a structured JSON error response."""
        from django.core.exceptions import (
            ObjectDoesNotExist,
            PermissionDenied,
            SuspiciousOperation,
            ValidationError,
        )

        request_id = get_current_request_id() or getattr(request, "request_id", "unknown")

        # Determine HTTP status and user-facing message
        if isinstance(exc, PermissionDenied):
            status_code = 403
            message = "You do not have permission to perform this action."
            log_level = "warning"
        elif isinstance(exc, ObjectDoesNotExist):
            status_code = 404
            message = "The requested resource was not found."
            log_level = "warning"
        elif isinstance(exc, SuspiciousOperation):
            status_code = 400
            message = "Bad request."
            log_level = "warning"
        elif isinstance(exc, ValidationError):
            status_code = 422
            message = "Validation failed."
            log_level = "warning"
        else:
            status_code = 500
            message = "An internal server error occurred. Please try again later."
            log_level = "error"

        # Log the exception
        log_data = {
            "request_id": request_id,
            "exception_type": type(exc).__name__,
            "exception_message": str(exc),
            "path": request.path,
            "method": request.method,
        }

        if log_level == "error":
            logger.error(
                "Unhandled exception",
                extra={"kavan_data": log_data},
                exc_info=True,
            )
        else:
            logger.warning(
                "Handled exception",
                extra={"kavan_data": log_data},
            )

        # Build standard error response
        error_response = {
            "success": False,
            "message": message,
            "data": None,
            "errors": [
                {
                    "code": "INTERNAL_SERVER_ERROR" if status_code == 500 else "REQUEST_ERROR",
                    "message": message,
                }
            ],
            "meta": {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "request_id": request_id,
                "version": "v1",
            },
        }

        return JsonResponse(error_response, status=status_code)
