"""
KAVAN v6.0 — Request/Response Logging Middleware
============================================================
Logs every HTTP request and response as structured JSON.

Logged fields:
  - request_id       (from RequestIDMiddleware)
  - method, path, query_string
  - ip_address       (respects X-Forwarded-For)
  - user_agent
  - user_id          (None until Layer 2 authentication)
  - status_code
  - response_time_ms
  - content_length

PII redaction:
  - Authorization headers are masked
  - Password fields in request body are masked
  - Sensitive query params are masked
"""

import json
import logging
import time
from typing import Optional

from django.conf import settings

logger = logging.getLogger("kavan")

# Fields to redact from request body
_SENSITIVE_BODY_FIELDS = frozenset({
    "password",
    "password_confirm",
    "new_password",
    "old_password",
    "token",
    "access_token",
    "refresh_token",
    "secret",
    "api_key",
    "credit_card",
    "cvv",
    "ssn",
})

# Query params to redact
_SENSITIVE_QUERY_PARAMS = frozenset({
    "token",
    "access_token",
    "refresh_token",
    "api_key",
    "secret",
    "password",
})

# Paths to skip logging (e.g. health probes from load balancers)
_SKIP_LOG_PATHS = frozenset({
    "/health/live/",
    "/health/ready/",
    "/static/",
    "/favicon.ico",
})


def _get_client_ip(request) -> str:
    """Extract client IP, respecting X-Forwarded-For from reverse proxy."""
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "unknown")


def _mask_sensitive_body(body_str: str) -> dict:
    """Parse JSON body and mask sensitive fields."""
    try:
        body = json.loads(body_str)
        if isinstance(body, dict):
            return {
                k: "***REDACTED***" if k in _SENSITIVE_BODY_FIELDS else v
                for k, v in body.items()
            }
        return body
    except (json.JSONDecodeError, UnicodeDecodeError):
        return {}


def _get_request_body(request) -> Optional[dict]:
    """Safely read and redact the request body."""
    if not getattr(settings, "LOG_REQUEST_BODY", False):
        return None
    try:
        if request.content_type and "application/json" in request.content_type:
            return _mask_sensitive_body(request.body.decode("utf-8", errors="replace"))
    except Exception:
        pass
    return None


class RequestLoggingMiddleware:
    """
    Structured JSON logging middleware for all HTTP requests.

    Logs at INFO level for successful responses,
    WARNING for 4xx, ERROR for 5xx.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip non-loggable paths
        if self._should_skip(request.path):
            return self.get_response(request)

        start_time = time.monotonic()
        request_id = getattr(request, "request_id", "unknown")

        # Process the request
        response = self.get_response(request)

        # Calculate elapsed time
        elapsed_ms = round((time.monotonic() - start_time) * 1000, 2)

        # Build log record
        log_data = {
            "request_id": request_id,
            "method": request.method,
            "path": request.path,
            "query_string": self._sanitize_query_string(request.META.get("QUERY_STRING", "")),
            "status_code": response.status_code,
            "response_time_ms": elapsed_ms,
            "ip_address": _get_client_ip(request),
            "user_agent": request.META.get("HTTP_USER_AGENT", ""),
            "content_length": response.get("Content-Length", 0),
            "user_id": self._get_user_id(request),
        }

        # Select log level based on status code
        if response.status_code >= 500:
            logger.error("HTTP request completed", extra={"kavan_data": log_data})
        elif response.status_code >= 400:
            logger.warning("HTTP request completed", extra={"kavan_data": log_data})
        else:
            logger.info("HTTP request completed", extra={"kavan_data": log_data})

        return response

    def _should_skip(self, path: str) -> bool:
        """Return True for paths that should not be logged."""
        return any(path.startswith(skip_path) for skip_path in _SKIP_LOG_PATHS)

    def _get_user_id(self, request) -> Optional[str]:
        """Extract user ID if authenticated (Layer 2 will populate this)."""
        user = getattr(request, "user", None)
        if user and hasattr(user, "id") and user.is_authenticated:
            return str(user.id)
        return None

    def _sanitize_query_string(self, query_string: str) -> str:
        """Mask sensitive query parameters."""
        if not query_string:
            return ""
        parts = []
        for param in query_string.split("&"):
            if "=" in param:
                key, _, value = param.partition("=")
                if key.lower() in _SENSITIVE_QUERY_PARAMS:
                    parts.append(f"{key}=***REDACTED***")
                else:
                    parts.append(param)
            else:
                parts.append(param)
        return "&".join(parts)
