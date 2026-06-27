"""
KAVAN v6.0 — Unit Tests: Utilities
"""

import pytest

from common.utils.helpers import (
    generate_uuid,
    mask_pii,
    truncate_string,
    to_snake_case,
    to_camel_case,
    safe_int,
    safe_str,
    deep_merge,
)


@pytest.mark.unit
class TestHelpers:

    def test_generate_uuid_is_string(self):
        result = generate_uuid()
        assert isinstance(result, str)

    def test_generate_uuid_is_unique(self):
        ids = {generate_uuid() for _ in range(100)}
        assert len(ids) == 100

    def test_mask_pii_email(self):
        masked = mask_pii("user@example.com")
        assert "@example.com" in masked
        assert "us***" in masked

    def test_mask_pii_phone(self):
        masked = mask_pii("9876543210", visible_chars=4)
        assert masked.endswith("3210")
        assert "***" in masked

    def test_mask_pii_empty(self):
        assert mask_pii("") == ""

    def test_truncate_string_under_limit(self):
        assert truncate_string("hello", 10) == "hello"

    def test_truncate_string_over_limit(self):
        result = truncate_string("hello world", max_length=8)
        assert len(result) == 8
        assert result.endswith("...")

    def test_to_snake_case(self):
        assert to_snake_case("CamelCaseString") == "camel_case_string"
        assert to_snake_case("HTTPSRequest") == "h_t_t_p_s_request"

    def test_to_camel_case(self):
        assert to_camel_case("snake_case_string") == "snakeCaseString"
        assert to_camel_case("my_var") == "myVar"

    def test_safe_int_valid(self):
        assert safe_int("42") == 42
        assert safe_int(3.7) == 3

    def test_safe_int_invalid(self):
        assert safe_int("abc") == 0
        assert safe_int(None) == 0
        assert safe_int("abc", default=99) == 99

    def test_safe_str_none(self):
        assert safe_str(None) == ""
        assert safe_str(None, default="N/A") == "N/A"

    def test_safe_str_value(self):
        assert safe_str(42) == "42"
        assert safe_str("hello") == "hello"

    def test_deep_merge_basic(self):
        base = {"a": 1, "b": {"c": 2}}
        override = {"b": {"d": 3}, "e": 4}
        result = deep_merge(base, override)
        assert result == {"a": 1, "b": {"c": 2, "d": 3}, "e": 4}

    def test_deep_merge_override_wins(self):
        base = {"a": 1}
        override = {"a": 99}
        result = deep_merge(base, override)
        assert result["a"] == 99

    def test_deep_merge_does_not_mutate(self):
        base = {"a": {"b": 1}}
        override = {"a": {"c": 2}}
        result = deep_merge(base, override)
        assert "b" in result["a"]
        assert "b" in base["a"]  # original not mutated
