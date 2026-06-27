"""
KAVAN v6.0 — Base API View
============================================================
All KAVAN views extend BaseAPIView, which provides:
  - request_id injection
  - Standard response helpers
  - Structured error handling
  - Logging per request
"""

import logging

from rest_framework.views import APIView
from rest_framework.request import Request

from common.responses.standard_response import StandardResponse

logger = logging.getLogger("kavan")


class BaseAPIView(APIView):
    """
    Abstract base view for all KAVAN API views.

    Provides standardized response helpers and request_id access.
    Views should NEVER return raw Response objects — always use
    the helpers below to ensure consistent envelope format.
    """

    def success(self, data=None, message="Operation successful.", status=200):
        """Return a standard success response."""
        return StandardResponse.success(
            data=data,
            message=message,
            status=status,
            request=self.request,
        )

    def created(self, data=None, message="Resource created successfully."):
        """Return a standard 201 Created response."""
        return StandardResponse.created(
            data=data,
            message=message,
            request=self.request,
        )

    def error(self, message, errors=None, status=400):
        """Return a standard error response."""
        return StandardResponse.error(
            message=message,
            errors=errors,
            status=status,
            request=self.request,
        )

    def not_found(self, message="Resource not found."):
        """Return a standard 404 Not Found response."""
        return StandardResponse.not_found(
            message=message,
            request=self.request,
        )

    @property
    def request_id(self) -> str:
        """Return the current request ID."""
        return getattr(self.request, "request_id", "")
