"""
KAVAN v6.0 — System Health View
============================================================
Exposes host OS resource utilization and process thread info.
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from datetime import datetime, timezone

from monitoring.registry import metrics_registry

class SystemHealthView(APIView):
    """
    GET /health/system/
    Returns real-time CPU, memory, disk usage, and thread metrics.
    """
    authentication_classes = []
    permission_classes = []

    def get(self, request: Request) -> Response:
        system_report = metrics_registry.collect_all()
        
        return Response(
            {
                "success": True,
                "message": "System resource metrics retrieved successfully.",
                "data": system_report,
                "errors": None,
                "meta": {
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "request_id": getattr(request, "request_id", ""),
                    "version": "v1",
                },
            },
            status=status.HTTP_200_OK,
        )
