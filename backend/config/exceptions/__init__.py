"""
KAVAN v6.0 — Exceptions Package
"""

from config.exceptions.base import KavanBaseException
from config.exceptions.auth import (
    AuthenticationException,
    TokenExpiredException,
    TokenInvalidException,
    PermissionDeniedException,
    AccountDisabledException,
    AccountLockedException,
    InvalidCredentialsException,
    SessionExpiredException,
)
from config.exceptions.validation import (
    ValidationException,
    FieldValidationException,
    RequiredFieldException,
    InvalidFormatException,
    DuplicateValueException,
)
from config.exceptions.business import (
    BusinessRuleException,
    ResourceNotFoundException,
    ConflictException,
    RateLimitExceededException,
    ServiceUnavailableException,
    OperationNotPermittedException,
    QuotaExceededException,
)

__all__ = [
    # Base
    "KavanBaseException",
    # Auth
    "AuthenticationException",
    "TokenExpiredException",
    "TokenInvalidException",
    "PermissionDeniedException",
    "AccountDisabledException",
    "AccountLockedException",
    "InvalidCredentialsException",
    "SessionExpiredException",
    # Validation
    "ValidationException",
    "FieldValidationException",
    "RequiredFieldException",
    "InvalidFormatException",
    "DuplicateValueException",
    # Business
    "BusinessRuleException",
    "ResourceNotFoundException",
    "ConflictException",
    "RateLimitExceededException",
    "ServiceUnavailableException",
    "OperationNotPermittedException",
    "QuotaExceededException",
]
