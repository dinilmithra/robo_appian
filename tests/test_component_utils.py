"""
Unit tests for ComponentUtils helper functions.

Tests XPath literal escaping, input validation, and core utility methods.
"""

import pytest

from robo_appian.utils.ComponentUtils import ComponentUtils


class TestXPathLiteral:
    """Tests for xpath_literal() XPath-safe string conversion."""

    def test_xpath_literal_simple_string(self):
        """Test simple string without quotes."""
        result = ComponentUtils.xpath_literal("test")
        assert result == '"test"'

    def test_xpath_literal_string_with_double_quotes(self):
        """Test string containing double quotes uses single quotes."""
        result = ComponentUtils.xpath_literal('test"value')
        assert result == "'test\"value'"

    def test_xpath_literal_string_with_single_quotes(self):
        """Test string containing single quotes uses double quotes."""
        result = ComponentUtils.xpath_literal("test'value")
        assert result == '"test\'value"'

    def test_xpath_literal_string_with_both_quotes(self):
        """Test string with both quotes uses concat() function."""
        result = ComponentUtils.xpath_literal('test"value\'mixed')
        # Should use concat to combine quoted segments
        assert "concat(" in result
        assert '\"test\"' in result

    def test_xpath_literal_empty_string(self):
        """Test empty string."""
        result = ComponentUtils.xpath_literal("")
        assert result == '""' or result == "''"

    def test_xpath_literal_nbsp_character(self):
        """Test string containing non-breaking space (NBSP)."""
        result = ComponentUtils.xpath_literal("test\u00a0value")
        assert "test\u00a0value" in result

    def test_xpath_literal_with_special_characters(self):
        """Test string with special XML/HTML characters."""
        result = ComponentUtils.xpath_literal("test<>&")
        assert "test<>&" in result


class TestInputValidation:
    """Tests for input validation helper methods."""

    def test_validate_text_input_valid_string(self):
        """Test valid string passes validation."""
        result = ComponentUtils.validate_text_input("valid text")
        assert result == "valid text"

    def test_validate_text_input_strips_whitespace(self):
        """Test leading/trailing whitespace is stripped."""
        result = ComponentUtils.validate_text_input("  valid text  ")
        assert result == "valid text"

    def test_validate_text_input_none_raises_error(self):
        """Test None value raises ValueError."""
        with pytest.raises(ValueError, match="cannot be None"):
            ComponentUtils.validate_text_input(None)

    def test_validate_text_input_empty_string_raises_error(self):
        """Test empty string raises ValueError."""
        with pytest.raises(ValueError, match="cannot be empty"):
            ComponentUtils.validate_text_input("")

    def test_validate_text_input_whitespace_only_raises_error(self):
        """Test whitespace-only string raises ValueError."""
        with pytest.raises(ValueError, match="cannot be empty"):
            ComponentUtils.validate_text_input("   \t\n  ")

    def test_validate_text_input_non_string_raises_error(self):
        """Test non-string input raises ValueError."""
        with pytest.raises(ValueError, match="must be a string"):
            ComponentUtils.validate_text_input(123)

    def test_validate_text_input_custom_param_name(self):
        """Test custom parameter name in error message."""
        with pytest.raises(ValueError, match="custom_param"):
            ComponentUtils.validate_text_input("", "custom_param")

    def test_validate_label_text_valid(self):
        """Test validate_label_text with valid input."""
        result = ComponentUtils.validate_label_text("Submit Button")
        assert result == "Submit Button"

    def test_validate_label_text_invalid(self):
        """Test validate_label_text with invalid input."""
        with pytest.raises(ValueError, match="label"):
            ComponentUtils.validate_label_text(None)

    def test_validate_id_valid(self):
        """Test validate_id with valid input."""
        result = ComponentUtils.validate_id("element_id_123")
        assert result == "element_id_123"

    def test_validate_id_invalid(self):
        """Test validate_id with invalid input."""
        with pytest.raises(ValueError, match="element_id"):
            ComponentUtils.validate_id("")


class TestRetryUntil:
    """Tests for retry_until() resilience utility."""

    def test_retry_until_succeeds_immediately(self):
        """Test function succeeds on first attempt."""
        result = ComponentUtils.retry_until(lambda: True, timeout=1)
        assert result is True

    def test_retry_until_succeeds_after_retries(self):
        """Test function succeeds after retries."""
        attempt_count = {"count": 0}

        def failing_then_success():
            attempt_count["count"] += 1
            return attempt_count["count"] >= 2

        result = ComponentUtils.retry_until(failing_then_success, timeout=2, wait_interval=0.1)
        assert result is True
        assert attempt_count["count"] >= 2

    def test_retry_until_timeout_returns_default(self):
        """Test timeout returns default timeout_result."""
        result = ComponentUtils.retry_until(
            lambda: False,
            timeout=0.2,
            wait_interval=0.1,
            timeout_result="timed_out"
        )
        assert result == "timed_out"

    def test_retry_until_timeout_raises_error(self):
        """Test timeout raises error when raise_on_timeout is True."""
        with pytest.raises(TimeoutError):
            ComponentUtils.retry_until(
                lambda: False,
                timeout=0.2,
                wait_interval=0.1,
                raise_on_timeout=True
            )

    def test_retry_until_non_timeout_exception_raised_immediately(self):
        """Test non-timeout exceptions are raised immediately without retry."""
        attempt_count = {"count": 0}

        def failing_operation():
            attempt_count["count"] += 1
            raise ValueError("custom error")

        with pytest.raises(ValueError, match="custom error"):
            ComponentUtils.retry_until(failing_operation, timeout=1)

        # Should fail immediately, only 1 attempt
        assert attempt_count["count"] == 1


class TestDateUtilities:
    """Tests for date utility methods."""

    def test_today_format(self):
        """Test today() returns MM/DD/YYYY format."""
        result = ComponentUtils.today()
        # Should match MM/DD/YYYY pattern
        parts = result.split("/")
        assert len(parts) == 3
        assert len(parts[0]) == 2  # MM
        assert len(parts[1]) == 2  # DD
        assert len(parts[2]) == 4  # YYYY

    def test_yesterday_format(self):
        """Test yesterday() returns MM/DD/YYYY format."""
        result = ComponentUtils.yesterday()
        # Should match MM/DD/YYYY pattern
        parts = result.split("/")
        assert len(parts) == 3
        assert len(parts[0]) == 2  # MM
        assert len(parts[1]) == 2  # DD
        assert len(parts[2]) == 4  # YYYY

    def test_yesterday_is_before_today(self):
        """Test yesterday() date is before today()."""
        today = ComponentUtils.today()
        yesterday = ComponentUtils.yesterday()
        # String comparison works for MM/DD/YYYY format
        assert yesterday <= today


class TestGetVersion:
    """Tests for get_version() utility."""

    def test_get_version_format(self):
        """Test get_version returns semantic version string."""
        version = ComponentUtils.get_version()
        # Should return format like "0.0.2" or "0.0.0" if unable to read
        parts = version.split(".")
        assert len(parts) >= 2  # At minimum major.minor
        # All parts should be numeric strings
        for part in parts:
            assert part.isdigit()

    def test_get_version_not_empty(self):
        """Test get_version returns non-empty string."""
        version = ComponentUtils.get_version()
        assert isinstance(version, str)
        assert len(version) > 0
