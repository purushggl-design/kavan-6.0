"""
KAVAN v6.0 — Unit Tests: Validators
"""

import pytest

from config.validators.email import (
    validate_email_format,
    validate_email_domain,
    normalize_email,
    get_email_error_message,
)
from config.validators.password import (
    validate_password_strength,
    validate_password_match,
)
from config.validators.custom import (
    validate_uuid,
    validate_slug,
    validate_url,
    validate_positive_integer,
)


# ============================================================
# EMAIL VALIDATORS
# ============================================================

@pytest.mark.unit
class TestEmailValidators:

    def test_valid_email_formats(self):
        valid_emails = [
            "user@example.com",
            "user.name@example.co.uk",
            "user+tag@gmail.com",
            "user123@domain.org",
        ]
        for email in valid_emails:
            assert validate_email_format(email), f"Expected {email} to be valid"

    def test_invalid_email_formats(self):
        invalid_emails = [
            "not-an-email",
            "@nodomain.com",
            "user@",
            "user @example.com",
            "",
            None,
        ]
        for email in invalid_emails:
            assert not validate_email_format(email), f"Expected {email} to be invalid"

    def test_disposable_email_blocked(self):
        assert not validate_email_domain("user@mailinator.com", block_disposable=True)
        assert not validate_email_domain("test@guerrillamail.com", block_disposable=True)

    def test_disposable_email_allowed_when_not_blocking(self):
        assert validate_email_domain("user@mailinator.com", block_disposable=False)

    def test_normalize_email_lowercases(self):
        assert normalize_email("USER@EXAMPLE.COM") == "user@example.com"

    def test_normalize_email_strips_spaces(self):
        assert normalize_email("  user@example.com  ") == "user@example.com"

    def test_get_email_error_message_valid(self):
        assert get_email_error_message("user@example.com") is None

    def test_get_email_error_message_invalid(self):
        error = get_email_error_message("invalid-email")
        assert error is not None
        assert "valid" in error.lower()

    def test_get_email_error_message_empty(self):
        error = get_email_error_message("")
        assert error is not None
        assert "required" in error.lower()


# ============================================================
# PASSWORD VALIDATORS
# ============================================================

@pytest.mark.unit
class TestPasswordValidators:

    def test_strong_password_passes(self):
        result = validate_password_strength("MyStr0ng@Pass2024!")
        assert result.is_valid
        assert result.score > 60
        assert len(result.errors) == 0

    def test_short_password_fails(self):
        result = validate_password_strength("Short1!")
        assert not result.is_valid
        assert any("at least" in e for e in result.errors)

    def test_common_password_fails(self):
        result = validate_password_strength("password123!")
        assert not result.is_valid
        assert any("common" in e.lower() for e in result.errors)

    def test_no_uppercase_fails(self):
        result = validate_password_strength("my_str0ng@pass2024")
        assert not result.is_valid
        assert any("uppercase" in e for e in result.errors)

    def test_no_digit_fails(self):
        result = validate_password_strength("MyStrong@PassWord!")
        assert not result.is_valid
        assert any("digit" in e for e in result.errors)

    def test_no_special_char_fails(self):
        result = validate_password_strength("MyStr0ngPassw0rd")
        assert not result.is_valid
        assert any("special" in e for e in result.errors)

    def test_password_match_success(self):
        error = validate_password_match("MyPass123!", "MyPass123!")
        assert error is None

    def test_password_match_failure(self):
        error = validate_password_match("MyPass123!", "Different!")
        assert error is not None
        assert "match" in error.lower()


# ============================================================
# CUSTOM VALIDATORS
# ============================================================

@pytest.mark.unit
class TestCustomValidators:

    def test_valid_uuid(self):
        import uuid
        assert validate_uuid(str(uuid.uuid4()))

    def test_invalid_uuid(self):
        assert not validate_uuid("not-a-uuid")
        assert not validate_uuid("12345")
        assert not validate_uuid("")

    def test_valid_slugs(self):
        assert validate_slug("hello-world")
        assert validate_slug("my-slug-123")
        assert validate_slug("singleword")

    def test_invalid_slugs(self):
        assert not validate_slug("Hello-World")  # uppercase
        assert not validate_slug("has spaces")
        assert not validate_slug("-starts-with-dash")
        assert not validate_slug("ends-with-dash-")

    def test_valid_urls(self):
        assert validate_url("https://example.com")
        assert validate_url("http://localhost:8000")
        assert validate_url("https://example.com/path?query=1")

    def test_invalid_urls(self):
        assert not validate_url("ftp://example.com")
        assert not validate_url("not-a-url")
        assert not validate_url("")

    def test_positive_integer_valid(self):
        assert validate_positive_integer(1)
        assert validate_positive_integer("100")

    def test_positive_integer_invalid(self):
        assert not validate_positive_integer(0)
        assert not validate_positive_integer(-1)
        assert not validate_positive_integer("abc")
        assert not validate_positive_integer(None)
