"""Unit tests for LabelUtils."""

import pytest
from unittest.mock import MagicMock, patch

from robo_appian.components.LabelUtils import LabelUtils


def make_wait():
    wait = MagicMock()
    wait._driver = MagicMock()
    return wait


class TestClickByLabelText:
    @patch("robo_appian.components.LabelUtils.ComponentUtils.waitForComponentToBeVisibleByXpath")
    @patch("robo_appian.components.LabelUtils.ComponentUtils.click")
    def test_finds_and_clicks(self, mock_click, mock_find):
        wait = make_wait()
        mock_el = MagicMock()
        mock_find.return_value = mock_el
        LabelUtils.clickByLabelText(wait, "Expand")
        mock_click.assert_called_once_with(wait, mock_el)

    @patch("robo_appian.components.LabelUtils.ComponentUtils.waitForComponentToBeVisibleByXpath")
    @patch("robo_appian.components.LabelUtils.ComponentUtils.click")
    def test_xpath_uses_normalize_space_and_nbsp(self, mock_click, mock_find):
        wait = make_wait()
        mock_find.return_value = MagicMock()
        LabelUtils.clickByLabelText(wait, "Show Details")
        xpath = mock_find.call_args[0][1]
        assert "normalize-space" in xpath
        assert "Show Details" in xpath
        # NBSP translation should be present
        assert "\u00a0" in xpath or "translate" in xpath


class TestIsLabelExists:
    @patch("robo_appian.components.LabelUtils.ComponentUtils.waitForComponentToBeVisibleByXpath")
    def test_returns_true_when_label_found(self, mock_find):
        mock_find.return_value = MagicMock()
        wait = make_wait()
        assert LabelUtils.isLabelExists(wait, "Success!") is True

    @patch("robo_appian.components.LabelUtils.ComponentUtils.waitForComponentToBeVisibleByXpath")
    def test_returns_false_when_exception(self, mock_find):
        mock_find.side_effect = Exception("not found")
        wait = make_wait()
        assert LabelUtils.isLabelExists(wait, "Missing Label") is False

    @patch("robo_appian.components.LabelUtils.ComponentUtils.waitForComponentToBeVisibleByXpath")
    def test_does_not_raise_on_failure(self, mock_find):
        mock_find.side_effect = Exception("timeout")
        wait = make_wait()
        # Should not raise, just return False
        result = LabelUtils.isLabelExists(wait, "anything")
        assert result is False
