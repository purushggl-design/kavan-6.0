"""
KAVAN v6.0 — Custom Validators
"""

import re
import uuid
from typing import Optional


def validate_uuid(value: str) -> bool:
    """Return True if the value is a valid UUID."""
    try:
        uuid.UUID(str(value))
        return True
    except (ValueError, AttributeError):
        return False


def validate_phone_number(phone: str, country_code: str = "IN") -> bool:
    """
    Validate phone number format.

    Supports international format with country code prefix.
    Default: Indian mobile numbers (+91XXXXXXXXXX).
    """
    # Strip whitespace and dashes
    phone = re.sub(r"[\s\-()]", "", phone)

    # International format: +[country_code][number]
    international_pattern = re.compile(r"^\+\d{1,3}\d{6,14}$")
    if international_pattern.match(phone):
        return True

    # Indian mobile (10 digits starting with 6-9)
    if country_code == "IN":
        return bool(re.match(r"^[6-9]\d{9}$", phone))

    # Generic: 7-15 digits
    return bool(re.match(r"^\d{7,15}$", phone))


def validate_slug(value: str) -> bool:
    """Return True if the value is a valid URL slug (lowercase, hyphens)."""
    return bool(re.match(r"^[a-z0-9]+(?:-[a-z0-9]+)*$", value))


def validate_url(url: str) -> bool:
    """Return True if the value is a valid HTTP/HTTPS URL."""
    pattern = re.compile(
        r"^https?://"
        r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|"
        r"localhost|"
        r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
        r"(?::\d+)?"
        r"(?:/?|[/?]\S+)$",
        re.IGNORECASE,
    )
    return bool(pattern.match(url))


def validate_positive_integer(value) -> bool:
    """Return True if the value is a positive integer."""
    try:
        return int(value) > 0
    except (ValueError, TypeError):
        return False


def validate_non_empty_string(value: Optional[str]) -> bool:
    """Return True if the value is a non-empty string."""
    return bool(value and value.strip())


def validate_json_size(data: str, max_bytes: int = 65536) -> bool:
    """Return True if the JSON string is within the size limit (default 64KB)."""
    return len(data.encode("utf-8")) <= max_bytes
