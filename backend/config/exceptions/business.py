"""
KAVAN v6.0 — Business Rule Exception Classes
"""

from config.exceptions.base import KavanBaseException


class BusinessRuleException(KavanBaseException):
    """Raised when a business rule is violated."""
    http_status = 422
    code = "BUSINESS_RULE_VIOLATION"
    message = "The requested operation violates a business rule."


class ResourceNotFoundException(KavanBaseException):
    """Raised when a requested resource does not exist."""
    http_status = 404
    code = "RESOURCE_NOT_FOUND"
    message = "The requested resource was not found."

    def __init__(self, resource_type: str = "Resource", resource_id=None, **kwargs):
        if resource_id:
            message = f"{resource_type} with ID '{resource_id}' was not found."
        else:
            message = f"{resource_type} was not found."
        super().__init__(message=message, **kwargs)


class ConflictException(KavanBaseException):
    """Raised when the request conflicts with the current resource state."""
    http_status = 409
    code = "CONFLICT"
    message = "The request conflicts with the current state of the resource."


class RateLimitExceededException(KavanBaseException):
    """Raised when rate limits are exceeded."""
    http_status = 429
    code = "RATE_LIMIT_EXCEEDED"
    message = "Too many requests. Please slow down and try again later."


class ServiceUnavailableException(KavanBaseException):
    """Raised when a dependent service is unavailable."""
    http_status = 503
    code = "SERVICE_UNAVAILABLE"
    message = "The service is temporarily unavailable. Please try again later."


class OperationNotPermittedException(KavanBaseException):
    """Raised when an operation is not permitted in the current context."""
    http_status = 422
    code = "OPERATION_NOT_PERMITTED"
    message = "This operation is not permitted."


class QuotaExceededException(KavanBaseException):
    """Raised when a usage quota is exceeded (Layer 3 — multi-tenancy)."""
    http_status = 402
    code = "QUOTA_EXCEEDED"
    message = "You have exceeded your usage quota."
