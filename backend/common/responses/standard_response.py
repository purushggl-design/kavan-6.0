"""
KAVAN v6.0 — Standard API Response Builder
============================================================
All API responses follow a consistent envelope format.

Success response:
{
    "success": true,
    "message": "...",
    "data": { ... },
    "errors": null,
    "meta": {
        "timestamp": "...",
        "request_id": "...",
        "version": "v1"
    }
}

Error response:
{
    "success": false,
    "message": "...",
    "data": null,
    "errors": [{"field": "...", "code": "...", "message": "..."}],
    "meta": { ... }
}

Paginated response:
{
    "success": true,
    "message": "...",
    "data": [...],
    "errors": null,
    "meta": {
        "timestamp": "...",
        "request_id": "...",
        "version": "v1",
        "pagination": {
            "page": 1,
            "page_size": 20,
            "total_count": 100,
            "total_pages": 5,
            "has_next": true,
            "has_previous": false
        }
    }
}
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Union

from rest_framework.response import Response

from config.middleware.request_id import get_current_request_id


def _build_meta(request=None, version: str = "v1") -> Dict[str, Any]:
    """Build the standard meta object."""
    request_id = get_current_request_id()
    if not request_id and request:
        request_id = getattr(request, "request_id", "")
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "request_id": request_id,
        "version": version,
    }


class StandardResponse:
    """
    Factory class for building KAVAN standard API responses.

    All public methods return DRF Response objects with the
    standard envelope format.
    """

    @staticmethod
    def success(
        data: Any = None,
        message: str = "Operation successful.",
        status: int = 200,
        request=None,
        version: str = "v1",
    ) -> Response:
        """Build a successful API response."""
        return Response(
            {
                "success": True,
                "message": message,
                "data": data,
                "errors": None,
                "meta": _build_meta(request, version),
            },
            status=status,
        )

    @staticmethod
    def created(
        data: Any = None,
        message: str = "Resource created successfully.",
        request=None,
        version: str = "v1",
    ) -> Response:
        """Build a 201 Created response."""
        return StandardResponse.success(
            data=data,
            message=message,
            status=201,
            request=request,
            version=version,
        )

    @staticmethod
    def error(
        message: str = "An error occurred.",
        errors: Optional[List[Dict[str, Any]]] = None,
        status: int = 400,
        request=None,
        version: str = "v1",
    ) -> Response:
        """Build an error API response."""
        return Response(
            {
                "success": False,
                "message": message,
                "data": None,
                "errors": errors or [],
                "meta": _build_meta(request, version),
            },
            status=status,
        )

    @staticmethod
    def not_found(
        message: str = "Resource not found.",
        request=None,
    ) -> Response:
        """Build a 404 Not Found response."""
        return StandardResponse.error(
            message=message,
            errors=[{"code": "RESOURCE_NOT_FOUND", "message": message}],
            status=404,
            request=request,
        )

    @staticmethod
    def paginated(
        data: List[Any],
        pagination_meta: Dict[str, Any],
        message: str = "Data retrieved successfully.",
        status: int = 200,
        request=None,
        version: str = "v1",
    ) -> Response:
        """Build a paginated API response."""
        meta = _build_meta(request, version)
        meta["pagination"] = pagination_meta
        return Response(
            {
                "success": True,
                "message": message,
                "data": data,
                "errors": None,
                "meta": meta,
            },
            status=status,
        )

    @staticmethod
    def no_content() -> Response:
        """Build a 204 No Content response."""
        return Response(status=204)

    @staticmethod
    def from_exception(
        exc,
        request=None,
    ) -> Response:
        """
        Build an error response from a KavanBaseException.
        """
        from config.exceptions.base import KavanBaseException

        if isinstance(exc, KavanBaseException):
            return StandardResponse.error(
                message=exc.message,
                errors=exc.to_error_list(),
                status=exc.http_status,
                request=request,
            )
        return StandardResponse.error(
            message=str(exc),
            errors=[{"code": "INTERNAL_ERROR", "message": str(exc)}],
            status=500,
            request=request,
        )
