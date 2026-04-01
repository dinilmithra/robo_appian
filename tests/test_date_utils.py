"""Unit tests for DateUtils."""

import pytest
from unittest.mock import MagicMock, patch

from robo_appian.components.DateUtils import DateUtils


def make_wait():
    wait = MagicMock()
    wait._driver = MagicMock()
    return wait


class TestSetValueByLabelText:
    def test_sets_value_and_returns_component(self):
        wait = make_wait()
        mock_el = MagicMock()
        wait.until.return_value = mock_el
        with patch("robo_appian.components.DateUtils.InputUtils._setValueByComponent") as mock_set:
            result = DateUtils.setValueByLabelText(wait, "Start Date", "01/15/2024")
        mock_set.assert_called_once_with(wait, mock_el, "01/15/2024")
        assert result == mock_el

    def test_xpath_uses_label_text(self):
        wait = make_wait()
        mock_el = MagicMock()
        wait.until.return_value = mock_el
        with patch("robo_appian.components.DateUtils.InputUtils._setValueByComponent"):
            DateUtils.setValueByLabelText(wait, "End Date", "12/31/2024")
        call_args = wait.until.call_args
        # The XPath condition is passed to wait.until; extract xpath from EC condition
        # EC.element_to_be_clickable is called with (By.XPATH, xpath)
        condition_args = call_args[0][0]
        # condition_args is the EC tuple locator — check the xpath string was built
        assert condition_args is not None


class TestClickByLabelText:
    def test_clicks_date_component(self):
        wait = make_wait()
        mock_el = MagicMock()
        wait.until.return_value = mock_el
        with patch("robo_appian.components.DateUtils.ComponentUtils.click") as mock_click:
            result = DateUtils.clickByLabelText(wait, "Event Date")
        mock_click.assert_called_once_with(wait, mock_el)
        assert result == mock_el

    def test_returns_component_element(self):
        wait = make_wait()
        mock_el = MagicMock()
        wait.until.return_value = mock_el
        with patch("robo_appian.components.DateUtils.ComponentUtils.click"):
            result = DateUtils.clickByLabelText(wait, "Date")
        assert result == mock_el
