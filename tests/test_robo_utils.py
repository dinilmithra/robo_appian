"""Unit tests for RoboUtils."""

import pytest
from unittest.mock import MagicMock, patch
from selenium.common.exceptions import TimeoutException

from robo_appian.utils.RoboUtils import RoboUtils


class TestRetryOnTimeout:
    def test_succeeds_on_first_try(self):
        operation = MagicMock(return_value="result")
        result = RoboUtils.retry_on_timeout(operation, max_retries=3)
        assert result == "result"
        operation.assert_called_once()

    def test_retries_on_timeout_exception(self):
        operation = MagicMock(
            side_effect=[TimeoutException(), TimeoutException(), "success"]
        )
        result = RoboUtils.retry_on_timeout(operation, max_retries=3)
        assert result == "success"
        assert operation.call_count == 3

    def test_raises_timeout_after_max_retries(self):
        operation = MagicMock(side_effect=TimeoutException("timed out"))
        with pytest.raises(TimeoutException):
            RoboUtils.retry_on_timeout(operation, max_retries=3)
        assert operation.call_count == 3

    def test_reraises_non_timeout_exception_immediately(self):
        operation = MagicMock(side_effect=ValueError("bad value"))
        with pytest.raises(ValueError, match="bad value"):
            RoboUtils.retry_on_timeout(operation, max_retries=3)
        operation.assert_called_once()

    def test_custom_max_retries(self):
        operation = MagicMock(side_effect=TimeoutException())
        with pytest.raises(TimeoutException):
            RoboUtils.retry_on_timeout(operation, max_retries=5)
        assert operation.call_count == 5

    def test_max_retries_one_no_retry(self):
        operation = MagicMock(side_effect=TimeoutException())
        with pytest.raises(TimeoutException):
            RoboUtils.retry_on_timeout(operation, max_retries=1)
        operation.assert_called_once()

    def test_operation_name_in_error_message(self):
        operation = MagicMock(side_effect=TimeoutException("original"))
        with pytest.raises(TimeoutException) as exc_info:
            RoboUtils.retry_on_timeout(operation, max_retries=2, operation_name="my_op")
        assert "my_op" in str(exc_info.value)

    def test_returns_falsy_value_from_operation(self):
        operation = MagicMock(return_value=0)
        result = RoboUtils.retry_on_timeout(operation, max_retries=3)
        assert result == 0
