"""
KAVAN v6.0 — Utility Helpers
"""

import hashlib
import ipaddress
import re
import uuid
from datetime import datetime, timezone
from typing import Any, Optional


def generate_uuid() -> str:
    """Generate a new UUID4 string."""
    return str(uuid.uuid4())


def get_client_ip(request) -> str:
    """
    Extract the client's real IP address from request.
    Respects X-Forwarded-For header from reverse proxies.
    """
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        # Take the first IP (leftmost = original client)
        ip = x_forwarded_for.split(",")[0].strip()
        try:
            ipaddress.ip_address(ip)
            return ip
        except ValueError:
            pass
    return request.META.get("REMOTE_ADDR", "unknown")


def mask_pii(value: str, visible_chars: int = 4) -> str:
    """
    Mask a PII value (email, phone, etc.) showing only the last N characters.

    Example:
        mask_pii("user@example.com") → "***@example.com"
        mask_pii("9876543210", 4)   → "******3210"
    """
    if not value:
        return ""
    if "@" in value:
        local, domain = value.split("@", 1)
        masked_local = "***" if len(local) <= visible_chars else local[:2] + "***"
        return f"{masked_local}@{domain}"
    if len(value) <= visible_chars:
        return "***"
    return "***" + value[-visible_chars:]


def truncate_string(value: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate a string to max_length, appending suffix if truncated."""
    if not value or len(value) <= max_length:
        return value
    return value[: max_length - len(suffix)] + suffix


def now_utc() -> datetime:
    """Return the current UTC datetime (timezone-aware)."""
    return datetime.now(timezone.utc)


def now_utc_iso() -> str:
    """Return the current UTC datetime as ISO 8601 string."""
    return now_utc().isoformat()


def safe_int(value: Any, default: int = 0) -> int:
    """Safely convert value to int, returning default on failure."""
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


def safe_str(value: Any, default: str = "") -> str:
    """Safely convert value to string."""
    if value is None:
        return default
    return str(value)


def hash_value(value: str) -> str:
    """Return a SHA-256 hash of the value (for non-sensitive hashing)."""
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def to_snake_case(name: str) -> str:
    """Convert CamelCase to snake_case."""
    s1 = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def to_camel_case(name: str) -> str:
    """Convert snake_case to camelCase."""
    components = name.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


def deep_merge(base: dict, override: dict) -> dict:
    """
    Deep merge two dictionaries. Override values take priority.
    """
    result = base.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result
