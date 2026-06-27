"""
KAVAN v6.0 — Custom Pagination
============================================================
Standard pagination with KAVAN response envelope.

Response structure:
{
    "success": true,
    "data": [...],
    "meta": {
        "pagination": {
            "page": 1,
            "page_size": 20,
            "total_count": 150,
            "total_pages": 8,
            "has_next": true,
            "has_previous": false,
            "next_url": "...",
            "previous_url": "..."
        }
    }
}
"""

import math
from datetime import datetime, timezone

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from config.middleware.request_id import get_current_request_id
from django.conf import settings


class KavanPageNumberPagination(PageNumberPagination):
    """
    Custom pagination that wraps results in the KAVAN standard envelope.
    """

    page_size = settings.API_PAGINATION_PAGE_SIZE if hasattr(settings, "API_PAGINATION_PAGE_SIZE") else 20
    page_size_query_param = "page_size"
    max_page_size = settings.API_MAX_PAGE_SIZE if hasattr(settings, "API_MAX_PAGE_SIZE") else 100
    page_query_param = "page"

    def get_paginated_response(self, data):
        """Return paginated data in the KAVAN standard envelope."""
        page_number = self.page.number
        total_count = self.page.paginator.count
        total_pages = math.ceil(total_count / self.get_page_size(self.request))

        pagination_meta = {
            "page": page_number,
            "page_size": self.get_page_size(self.request),
            "total_count": total_count,
            "total_pages": total_pages,
            "has_next": self.page.has_next(),
            "has_previous": self.page.has_previous(),
            "next_url": self.get_next_link(),
            "previous_url": self.get_previous_link(),
        }

        return Response({
            "success": True,
            "message": "Data retrieved successfully.",
            "data": data,
            "errors": None,
            "meta": {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "request_id": get_current_request_id(),
                "version": "v1",
                "pagination": pagination_meta,
            },
        })

    def get_paginated_response_schema(self, schema):
        """OpenAPI schema for paginated responses."""
        return {
            "type": "object",
            "properties": {
                "success": {"type": "boolean"},
                "message": {"type": "string"},
                "data": schema,
                "errors": {"type": "null"},
                "meta": {
                    "type": "object",
                    "properties": {
                        "pagination": {
                            "type": "object",
                            "properties": {
                                "page": {"type": "integer"},
                                "page_size": {"type": "integer"},
                                "total_count": {"type": "integer"},
                                "total_pages": {"type": "integer"},
                                "has_next": {"type": "boolean"},
                                "has_previous": {"type": "boolean"},
                                "next_url": {"type": "string", "nullable": True},
                                "previous_url": {"type": "string", "nullable": True},
                            },
                        }
                    },
                },
            },
        }
