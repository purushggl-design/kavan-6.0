"""
KAVAN v6.0 — Email Validators
"""

import re
from typing import Optional


# RFC 5322 compliant email regex
_EMAIL_REGEX = re.compile(
    r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+"
    r"@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?"
    r"(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*\.[a-zA-Z]{2,}$"
)

# Common disposable email domains to block
_DISPOSABLE_DOMAINS = frozenset({
    "mailinator.com",
    "guerrillamail.com",
    "10minutemail.com",
    "throwam.com",
    "yopmail.com",
    "trashmail.com",
    "fakeinbox.com",
    "sharklasers.com",
    "guerrillamailblock.com",
})


def validate_email_format(email: str) -> bool:
    """Return True if the email address has a valid format."""
    if not email or not isinstance(email, str):
        return False
    email = email.strip().lower()
    return bool(_EMAIL_REGEX.match(email))


def validate_email_domain(email: str, block_disposable: bool = True) -> bool:
    """
    Return True if the email domain is acceptable.

    Args:
        email:            Email address to validate
        block_disposable: If True, reject known disposable email domains
    """
    if not validate_email_format(email):
        return False

    if block_disposable:
        domain = email.split("@", 1)[1].lower()
        if domain in _DISPOSABLE_DOMAINS:
            return False

    return True


def normalize_email(email: str) -> str:
    """Return a normalized (lowercase, stripped) email address."""
    return email.strip().lower()


def get_email_error_message(email: str) -> Optional[str]:
    """
    Return a human-readable error message for an invalid email,
    or None if the email is valid.
    """
    if not email:
        return "Email address is required."
    if not validate_email_format(email):
        return "Please enter a valid email address."
    domain = email.split("@", 1)[1].lower()
    if domain in _DISPOSABLE_DOMAINS:
        return "Disposable email addresses are not allowed."
    return None
