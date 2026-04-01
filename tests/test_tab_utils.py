"""Unit tests for TabUtils."""

import pytest
from unittest.mock import MagicMock, patch
from selenium.common.exceptions import NoSuchElementException

from robo_appian.components.TabUtils import TabUtils


def make_wait():
    wait = MagicMock()
    wait._driver = MagicMock()
    return wait


class TestFindTabByLabelText:
    def test_returns_tab_element(self):
        wait = make_wait()
        mock_el = MagicMock()
        wait.until.return_value = mock_el
        result = TabUtils.findTabByLabelText(wait, "Details")
        assert result == mock_el

    def test_wait_until_called_with_visibility_condition(self):
        wait = make_wait()
        wait.until.return_value = MagicMock()
        TabUtils.findTabByLabelText(wait, "History")
        wait.until.assert_called_once()


class TestSelectTabByLabelText:
    def test_finds_and_clicks_tab(self):
        wait = make_wait()
        mock_el = MagicMock()
        wait.until.return_value = mock_el
        with patch("robo_appian.components.TabUtils.ComponentUtils.click") as mock_click:
            TabUtils.selectTabByLabelText(wait, "Summary")
        mock_click.assert_called_once_with(wait, mock_el)


class TestCheckTabSelectedByLabelText:
    def test_returns_true_when_selected(self):
        wait = make_wait()
        mock_tab_el = MagicMock()
        mock_selected_el = MagicMock()
        wait.until.return_value = mock_tab_el
        with patch(
            "robo_appian.components.TabUtils.ComponentUtils.findChildComponentByXpath",
            return_value=mock_selected_el,
        ):
            result = TabUtils.checkTabSelectedByLabelText(wait, "Active")
        assert result is True

    def test_returns_false_when_not_selected(self):
        wait = make_wait()
        mock_tab_el = MagicMock()
        wait.until.return_value = mock_tab_el
        with patch(
            "robo_appian.components.TabUtils.ComponentUtils.findChildComponentByXpath",
            side_effect=Exception("not found"),
        ):
            result = TabUtils.checkTabSelectedByLabelText(wait, "Inactive")
        assert result is False

    def test_selected_tab_span_text_used_in_xpath(self):
        wait = make_wait()
        mock_tab_el = MagicMock()
        wait.until.return_value = mock_tab_el
        captured = {}

        def capture_xpath(w, el, xpath):
            captured["xpath"] = xpath
            raise Exception("not found")

        with patch(
            "robo_appian.components.TabUtils.ComponentUtils.findChildComponentByXpath",
            side_effect=capture_xpath,
        ):
            TabUtils.checkTabSelectedByLabelText(wait, "SomeTab")

        assert "Selected Tab." in captured["xpath"]
