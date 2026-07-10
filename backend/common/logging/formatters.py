"""
KAVAN v6.0 — JSON Formatter for Structured Logging
"""

import json
import logging
import traceback
from datetime import datetime, timezone
from typing import Any, Dict

from config.middleware.request_id import get_current_request_id


class KavanJSONFormatter(logging.Formatter):
    """
    Formats log records as structured JSON for log aggregation.

    Output format:
    {
        "timestamp":      "2026-06-26T10:30:00.123Z",
        "level":          "INFO",
        "logger":         "kavan.apps.monitoring",
        "message":        "Health check completed",
        "request_id":     "550e8400-...",
        "module":         "views",
        "function":       "get",
        "line":           42,
        "extra":          { ... }    // from logger.info("msg", extra={"kavan_data": {...}})
        "exception":      "..."      // only on exceptions
    }
    """

    def format(self, record: logging.LogRecord) -> str:
        log_entry: Dict[str, Any] = {
            "timestamp": datetime.fromtimestamp(
                record.created, tz=timezone.utc
            ).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "request_id": get_current_request_id() or "",
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Include any kavan_data passed via extra=
        kavan_data = getattr(record, "kavan_data", None)
        if kavan_data:
            log_entry["extra"] = kavan_data

        # Format exception if present
        if record.exc_info:
            log_entry["exception"] = {
                "type": record.exc_info[0].__name__ if record.exc_info[0] else None,
                "message": str(record.exc_info[1]) if record.exc_info[1] else None,
                "traceback": traceback.format_exception(*record.exc_info),
            }

        try:
            return json.dumps(log_entry, default=str, ensure_ascii=False)
        except (TypeError, ValueError):
            # Fallback to string if JSON serialization fails
            return str(log_entry)
