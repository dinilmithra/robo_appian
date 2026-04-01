"""Unit tests for ButtonUtils."""

import pytest
from unittest.mock import MagicMock, patch

from robo_appian.components.ButtonUtils import ButtonUtils


def make_wait():
    wait = MagicMock()
    wait._driver = MagicMock()
    return wait


class TestClickByLabelText:
    @patch("robo_appian.components.ButtonUtils.ComponentUtils.waitForComponentToBeVisibleByXpath")
    @patch("robo_appian.components.ButtonUtils.ComponentUtils.click")
    def test_finds_and_clicks_button(self, mock_click, mock_find):
        wait = make_wait()
        mock_el = MagicMock()
        mock_find.return_value = mock_el
        ButtonUtils.clickByLabelText(wait, "Submit")
        mock_click.assert_called_once_with(wait, mock_el)

    @patch("robo_appian.components.ButtonUtils.ComponentUtils.waitForComponentToBeVisibleByXpath")
    @patch("robo_appian.components.ButtonUtils.ComponentUtils.click")
    def test_xpath_uses_normalize_space(self, mock_click, mock_find):
        wait = make_wait()
        mock_find.return_value = MagicMock()
        ButtonUtils.clickByLabelText(wait, "Save Changes")
        called_xpath = mock_find.call_args[0][1]
        assert "normalize-space" in called_xpath
        assert "Save Changes" in called_xpath


class TestClickByPartialLabelText:
    @patch("robo_appian.components.ButtonUtils.ComponentUtils.waitForComponentToBeVisibleByXpath")
    @patch("robo_appian.components.ButtonUtils.ComponentUtils.click")
    def test_finds_and_clicks_button(self, mock_click, mock_find):
        wait = make_wait()
        mock_el = MagicMock()
        mock_find.return_value = mock_el
        ButtonUtils.clickByPartialLabelText(wait, "Save")
        mock_click.assert_called_once_with(wait, mock_el)

    @patch("robo_appian.components.ButtonUtils.ComponentUtils.waitForComponentToBeVisibleByXpath")
    @patch("robo_appian.components.ButtonUtils.ComponentUtils.click")
    def test_xpath_uses_contains(self, mock_click, mock_find):
        wait = make_wait()
        mock_find.return_value = MagicMock()
        ButtonUtils.clickByPartialLabelText(wait, "Save")
        called_xpath = mock_find.call_args[0][1]
        assert "contains" in called_xpath
        assert "Save" in called_xpath


class TestClickById:
    def test_finds_and_clicks_by_id(self):
        wait = make_wait()
        mock_el = MagicMock()
        wait.until.return_value = mock_el
        with patch("robo_appian.components.ButtonUtils.ComponentUtils.click") as mock_click:
            ButtonUtils.clickById(wait, "btn-123")
            mock_click.assert_called_once_with(wait, mock_el)


class TestIsButtonExistsByLabelText:
    @patch("robo_appian.components.ButtonUtils.ComponentUtils.findComponentByXPath")
    def test_returns_true_when_button_found(self, mock_find):
        mock_find.return_value = MagicMock()
        wait = make_wait()
        assert ButtonUtils.isButtonExistsByLabelText(wait, "Delete") is True

    @patch("robo_appian.components.ButtonUtils.ComponentUtils.findComponentByXPath")
    def test_returns_false_when_exception(self, mock_find):
        mock_find.side_effect = Exception("not found")
        wait = make_wait()
        assert ButtonUtils.isButtonExistsByLabelText(wait, "Delete") is False

    @patch("robo_appian.components.ButtonUtils.ComponentUtils.findComponentByXPath")
    def test_xpath_uses_exact_label_match(self, mock_find):
        mock_find.return_value = MagicMock()
        wait = make_wait()
        ButtonUtils.isButtonExistsByLabelText(wait, "Cancel")
        xpath = mock_find.call_args[0][1]
        assert "Cancel" in xpath
        assert "normalize-space" in xpath


class TestIsButtonExistsByPartialLabelText:
    @patch("robo_appian.components.ButtonUtils.ComponentUtils.findComponentByXPath")
    def test_returns_true_when_found(self, mock_find):
        mock_find.return_value = MagicMock()
        wait = make_wait()
        assert ButtonUtils.isButtonExistsByPartialLabelText(wait, "Save") is True

    @patch("robo_appian.components.ButtonUtils.ComponentUtils.findComponentByXPath")
    def test_returns_false_when_not_found(self, mock_find):
        mock_find.side_effect = Exception("not found")
        wait = make_wait()
        assert ButtonUtils.isButtonExistsByPartialLabelText(wait, "Save") is False


class TestIsButtonExistsByPartialLabelTextAfterLoad:
    @patch("robo_appian.components.ButtonUtils.ComponentUtils.waitForComponentToBeVisibleByXpath")
    def test_returns_true_when_visible(self, mock_find):
        mock_find.return_value = MagicMock()
        wait = make_wait()
        assert ButtonUtils.isButtonExistsByPartialLabelTextAfterLoad(wait, "Submit") is True

    @patch("robo_appian.components.ButtonUtils.ComponentUtils.waitForComponentToBeVisibleByXpath")
    def test_returns_false_when_exception(self, mock_find):
        mock_find.side_effect = Exception("timeout")
        wait = make_wait()
        assert ButtonUtils.isButtonExistsByPartialLabelTextAfterLoad(wait, "Submit") is False


class TestWaitForButtonToBeVisibleByPartialLabelText:
    @patch("robo_appian.components.ButtonUtils.ComponentUtils.waitForComponentToBeVisibleByXpath")
    def test_returns_element(self, mock_find):
        mock_el = MagicMock()
        mock_find.return_value = mock_el
        wait = make_wait()
        result = ButtonUtils.waitForButtonToBeVisibleByPartialLabelText(wait, "Submit")
        assert result == mock_el

    @patch("robo_appian.components.ButtonUtils.ComponentUtils.waitForComponentToBeVisibleByXpath")
    def test_xpath_uses_contains(self, mock_find):
        mock_find.return_value = MagicMock()
        wait = make_wait()
        ButtonUtils.waitForButtonToBeVisibleByPartialLabelText(wait, "Submit")
        xpath = mock_find.call_args[0][1]
        assert "contains" in xpath
        assert "Submit" in xpath
