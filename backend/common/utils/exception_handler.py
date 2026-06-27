"""
KAVAN v6.0 — DRF Custom Exception Handler
============================================================
Converts DRF exceptions and KavanBaseException to the
KAVAN standard error response format.

Configured in settings via:
    REST_FRAMEWORK = {
        "EXCEPTION_HANDLER": "common.utils.exception_handler.kavan_exception_handler"
    }
"""

import logging
from datetime import datetime, timezone
from typing import Any, Dict, List

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler

from config.middleware.request_id import get_current_request_id

logger = logging.getLogger("kavan.error")


def kavan_exception_handler(exc, context) -> Response:
    """
    Custom DRF exception handler.
    Maps DRF and KAVAN exceptions to standard error envelope.
    """
    from config.exceptions.base import KavanBaseException

    request = context.get("request")
    request_id = get_current_request_id()

    # Handle KAVAN custom exceptions
    if isinstance(exc, KavanBaseException):
        logger.warning(
            f"KavanException: {exc.code} — {exc.message}",
            extra={
                "kavan_data": {
                    "request_id": request_id,
                    "exception_type": type(exc).__name__,
                    "code": exc.code,
                }
            },
        )
        return _build_error_response(
            message=exc.message,
            errors=exc.to_error_list(),
            status_code=exc.http_status,
            request_id=request_id,
        )

    # Fall back to DRF's handler for DRF exceptions
    drf_response = drf_exception_handler(exc, context)

    if drf_response is not None:
        errors = _extract_drf_errors(drf_response.data)
        message = _get_message_from_status(drf_response.status_code)

        logger.warning(
            f"DRF Exception: {type(exc).__name__} — {drf_response.status_code}",
            extra={"kavan_data": {"request_id": request_id}},
        )

        return _build_error_response(
            message=message,
            errors=errors,
            status_code=drf_response.status_code,
            request_id=request_id,
        )

    # Unhandled — let ExceptionHandlerMiddleware catch it
    return None


def _build_error_response(
    message: str,
    errors: List[Dict[str, Any]],
    status_code: int,
    request_id: str,
) -> Response:
    """Build the standard KAVAN error response envelope."""
    return Response(
        {
            "success": False,
            "message": message,
            "data": None,
            "errors": errors,
            "meta": {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "request_id": request_id,
                "version": "v1",
            },
        },
        status=status_code,
    )


def _extract_drf_errors(data) -> List[Dict[str, Any]]:
    """Convert DRF error data to KAVAN error list format."""
    errors = []
    if isinstance(data, dict):
        for field, messages in data.items():
            if isinstance(messages, list):
                for msg in messages:
                    errors.append({
                        "field": field if field != "non_field_errors" else None,
                        "code": "VALIDATION_ERROR",
                        "message": str(msg),
                    })
            else:
                errors.append({
                    "field": field if field != "non_field_errors" else None,
                    "code": "VALIDATION_ERROR",
                    "message": str(messages),
                })
    elif isinstance(data, list):
        for msg in data:
            errors.append({"code": "VALIDATION_ERROR", "message": str(msg)})
    else:
        errors.append({"code": "VALIDATION_ERROR", "message": str(data)})
    return errors


def _get_message_from_status(status_code: int) -> str:
    """Return a user-friendly message for common HTTP status codes."""
    messages = {
        400: "The request is invalid.",
        401: "Authentication is required.",
        403: "You do not have permission to perform this action.",
        404: "The requested resource was not found.",
        405: "Method not allowed.",
        409: "Conflict with the current state of the resource.",
        422: "Validation failed.",
        429: "Too many requests. Please slow down.",
        500: "An internal server error occurred.",
        503: "Service temporarily unavailable.",
    }
    return messages.get(status_code, "An error occurred.")
