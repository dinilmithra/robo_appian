"""Unit tests for MyCustomError exception."""

import pytest
from robo_appian.exceptions.MyCustomError import MyCustomError


class TestMyCustomError:
    def test_is_exception_subclass(self):
        assert issubclass(MyCustomError, Exception)

    def test_default_message(self):
        err = MyCustomError()
        assert err.message == "This is a custom error!"
        assert str(err) == "This is a custom error!"

    def test_custom_message(self):
        err = MyCustomError("Something went wrong")
        assert err.message == "Something went wrong"
        assert str(err) == "Something went wrong"

    def test_can_be_raised_and_caught(self):
        with pytest.raises(MyCustomError) as exc_info:
            raise MyCustomError("test error")
        assert exc_info.value.message == "test error"

    def test_can_be_caught_as_generic_exception(self):
        with pytest.raises(Exception):
            raise MyCustomError("generic catch")
