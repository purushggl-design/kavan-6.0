"""
KAVAN v6.0 — Validation Exception Classes
"""

from typing import Any, Dict, List, Optional

from config.exceptions.base import KavanBaseException


class ValidationException(KavanBaseException):
    """
    Raised when request data fails validation.
    Can carry a list of field-level errors.
    """
    http_status = 422
    code = "VALIDATION_ERROR"
    message = "The provided data is invalid."

    def __init__(
        self,
        message: Optional[str] = None,
        field_errors: Optional[List[Dict[str, Any]]] = None,
        **kwargs,
    ):
        super().__init__(message=message, **kwargs)
        self._field_errors = field_errors or []

    def to_error_list(self) -> List[Dict[str, Any]]:
        if self._field_errors:
            return self._field_errors
        return super().to_error_list()


class FieldValidationException(KavanBaseException):
    """Raised for a single field validation failure."""
    http_status = 422
    code = "FIELD_VALIDATION_ERROR"

    def __init__(
        self,
        field: str,
        message: str,
        code: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(message=message, code=code, **kwargs)
        self.field = field

    def to_dict(self) -> Dict[str, Any]:
        return {
            "field": self.field,
            "code": self.code,
            "message": self.message,
        }


class RequiredFieldException(FieldValidationException):
    """Raised when a required field is missing."""
    code = "REQUIRED_FIELD"

    def __init__(self, field: str, **kwargs):
        super().__init__(
            field=field,
            message=f"The field '{field}' is required.",
            **kwargs,
        )


class InvalidFormatException(FieldValidationException):
    """Raised when a field value has an invalid format."""
    code = "INVALID_FORMAT"


class DuplicateValueException(KavanBaseException):
    """Raised when a unique constraint is violated."""
    http_status = 409
    code = "DUPLICATE_VALUE"
    message = "A resource with this value already exists."
