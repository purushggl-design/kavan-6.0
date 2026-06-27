"""
KAVAN v6.0 — Password Validators
"""

import re
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class PasswordStrengthResult:
    """Result of a password strength check."""
    is_valid: bool
    score: int  # 0-100
    errors: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)


# Common weak passwords
_COMMON_PASSWORDS = frozenset({
    "password", "password123", "123456", "123456789", "qwerty",
    "abc123", "letmein", "monkey", "1234567890", "iloveyou",
    "admin", "welcome", "login", "pass", "master", "dragon",
    "111111", "baseball", "football", "shadow", "sunshine",
})

_SPECIAL_CHARS = frozenset("!@#$%^&*()_+-=[]{}|;':\",./<>?")


def validate_password_strength(
    password: str,
    min_length: int = 12,
    require_uppercase: bool = True,
    require_lowercase: bool = True,
    require_digits: bool = True,
    require_special: bool = True,
) -> PasswordStrengthResult:
    """
    Validate password against configurable strength requirements.

    Returns a PasswordStrengthResult with score (0-100), errors, and suggestions.
    """
    errors: List[str] = []
    suggestions: List[str] = []
    score = 0

    if not password:
        return PasswordStrengthResult(
            is_valid=False,
            score=0,
            errors=["Password is required."],
        )

    # Length check
    if len(password) < min_length:
        errors.append(f"Password must be at least {min_length} characters long.")
    else:
        score += 20
        if len(password) >= 16:
            score += 10
        if len(password) >= 20:
            score += 10

    # Common passwords
    if password.lower() in _COMMON_PASSWORDS:
        errors.append("This password is too common. Please choose a more unique one.")

    # Uppercase
    if require_uppercase and not re.search(r"[A-Z]", password):
        errors.append("Password must contain at least one uppercase letter.")
    elif re.search(r"[A-Z]", password):
        score += 15

    # Lowercase
    if require_lowercase and not re.search(r"[a-z]", password):
        errors.append("Password must contain at least one lowercase letter.")
    elif re.search(r"[a-z]", password):
        score += 15

    # Digits
    if require_digits and not re.search(r"\d", password):
        errors.append("Password must contain at least one digit.")
    elif re.search(r"\d", password):
        score += 15

    # Special characters
    if require_special and not any(c in _SPECIAL_CHARS for c in password):
        errors.append("Password must contain at least one special character (!@#$%^&*...).")
    elif any(c in _SPECIAL_CHARS for c in password):
        score += 15

    # Suggestions (non-blocking)
    if not re.search(r"[A-Z].*[A-Z]", password):
        suggestions.append("Use multiple uppercase letters for a stronger password.")
    if not re.search(r"\d.*\d", password):
        suggestions.append("Use multiple numbers for a stronger password.")

    is_valid = len(errors) == 0
    return PasswordStrengthResult(
        is_valid=is_valid,
        score=min(score, 100),
        errors=errors,
        suggestions=suggestions,
    )


def validate_password_match(password: str, confirm_password: str) -> Optional[str]:
    """Return an error message if passwords do not match, else None."""
    if password != confirm_password:
        return "Passwords do not match."
    return None
