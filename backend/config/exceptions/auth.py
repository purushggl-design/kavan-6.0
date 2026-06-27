"""
KAVAN v6.0 — Authentication & Authorization Exceptions
"""

from config.exceptions.base import KavanBaseException


class AuthenticationException(KavanBaseException):
    """Raised when authentication fails."""
    http_status = 401
    code = "AUTHENTICATION_FAILED"
    message = "Authentication credentials were not provided or are invalid."


class TokenExpiredException(KavanBaseException):
    """Raised when a JWT or session token has expired."""
    http_status = 401
    code = "TOKEN_EXPIRED"
    message = "Your session has expired. Please log in again."


class TokenInvalidException(KavanBaseException):
    """Raised when a token is malformed or tampered with."""
    http_status = 401
    code = "TOKEN_INVALID"
    message = "The provided token is invalid."


class PermissionDeniedException(KavanBaseException):
    """Raised when a user lacks permission for an action."""
    http_status = 403
    code = "PERMISSION_DENIED"
    message = "You do not have permission to perform this action."


class AccountDisabledException(KavanBaseException):
    """Raised when a user account is disabled."""
    http_status = 403
    code = "ACCOUNT_DISABLED"
    message = "Your account has been disabled. Please contact support."


class AccountLockedException(KavanBaseException):
    """Raised when a user account is locked after failed login attempts."""
    http_status = 403
    code = "ACCOUNT_LOCKED"
    message = "Your account is temporarily locked. Please try again later."


class InvalidCredentialsException(KavanBaseException):
    """Raised on invalid login credentials."""
    http_status = 401
    code = "INVALID_CREDENTIALS"
    message = "Invalid email or password."


class SessionExpiredException(KavanBaseException):
    """Raised when a user session has expired."""
    http_status = 401
    code = "SESSION_EXPIRED"
    message = "Your session has expired. Please log in again."
