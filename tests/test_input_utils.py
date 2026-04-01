"""Unit tests for InputUtils."""

import pytest
from unittest.mock import MagicMock, patch

from robo_appian.components.InputUtils import InputUtils


def make_wait():
    wait = MagicMock()
    wait._driver = MagicMock()
    return wait


def make_label_element(for_attr):
    el = MagicMock()
    el.get_attribute.side_effect = lambda a: for_attr if a == "for" else None
    return el


class TestSetValueByComponent:
    def test_clears_and_sends_keys(self):
        wait = make_wait()
        component = MagicMock()
        with patch("robo_appian.components.InputUtils.ActionChains") as MockAC:
            mock_actions = MagicMock()
            MockAC.return_value = mock_actions
            mock_actions.move_to_element.return_value = mock_actions
            InputUtils._setValueByComponent(wait, component, "hello")
        component.clear.assert_called_once()
        component.send_keys.assert_called_once_with("hello")

    def test_returns_component(self):
        wait = make_wait()
        component = MagicMock()
        with patch("robo_appian.components.InputUtils.ActionChains"):
            result = InputUtils._setValueByComponent(wait, component, "value")
        assert result is component


class TestSetValueByLabelText:
    @patch("robo_appian.components.InputUtils.ComponentUtils.waitForComponentToBeVisibleByXpath")
    @patch("robo_appian.components.InputUtils.ComponentUtils.findComponentById")
    def test_sets_value_via_label(self, mock_find_by_id, mock_find_label):
        wait = make_wait()
        label_el = make_label_element("input-id-1")
        input_el = MagicMock()
        mock_find_label.return_value = label_el
        mock_find_by_id.return_value = input_el
        with patch("robo_appian.components.InputUtils.ActionChains"):
            InputUtils.setValueByLabelText(wait, "Username", "john")
        input_el.send_keys.assert_called_once_with("john")

    @patch("robo_appian.components.InputUtils.ComponentUtils.waitForComponentToBeVisibleByXpath")
    def test_raises_value_error_when_no_for_attribute(self, mock_find_label):
        wait = make_wait()
        label_el = make_label_element(None)
        mock_find_label.return_value = label_el
        with pytest.raises(ValueError, match="'for' attribute"):
            InputUtils.setValueByLabelText(wait, "Username", "john")

    @patch("robo_appian.components.InputUtils.ComponentUtils.waitForComponentToBeVisibleByXpath")
    @patch("robo_appian.components.InputUtils.ComponentUtils.findComponentById")
    def test_xpath_uses_exact_normalize_space(self, mock_find_by_id, mock_find_label):
        wait = make_wait()
        mock_find_label.return_value = make_label_element("x")
        mock_find_by_id.return_value = MagicMock()
        with patch("robo_appian.components.InputUtils.ActionChains"):
            InputUtils.setValueByLabelText(wait, "Email", "e@example.com")
        xpath = mock_find_label.call_args[0][1]
        assert "normalize-space" in xpath
        assert "Email" in xpath


class TestSetValueByPartialLabelText:
    @patch("robo_appian.components.InputUtils.ComponentUtils.waitForComponentToBeVisibleByXpath")
    @patch("robo_appian.components.InputUtils.ComponentUtils.findComponentById")
    def test_sets_value_via_partial_label(self, mock_find_by_id, mock_find_label):
        wait = make_wait()
        label_el = make_label_element("partial-input")
        input_el = MagicMock()
        mock_find_label.return_value = label_el
        mock_find_by_id.return_value = input_el
        with patch("robo_appian.components.InputUtils.ActionChains"):
            InputUtils.setValueByPartialLabelText(wait, "User", "doe")
        input_el.send_keys.assert_called_once_with("doe")

    @patch("robo_appian.components.InputUtils.ComponentUtils.waitForComponentToBeVisibleByXpath")
    def test_raises_value_error_when_no_for_attribute(self, mock_find_label):
        wait = make_wait()
        mock_find_label.return_value = make_label_element(None)
        with pytest.raises(ValueError, match="'for' attribute"):
            InputUtils.setValueByPartialLabelText(wait, "User", "doe")

    @patch("robo_appian.components.InputUtils.ComponentUtils.waitForComponentToBeVisibleByXpath")
    @patch("robo_appian.components.InputUtils.ComponentUtils.findComponentById")
    def test_xpath_uses_contains(self, mock_find_by_id, mock_find_label):
        wait = make_wait()
        mock_find_label.return_value = make_label_element("x")
        mock_find_by_id.return_value = MagicMock()
        with patch("robo_appian.components.InputUtils.ActionChains"):
            InputUtils.setValueByPartialLabelText(wait, "Email", "e@e.com")
        xpath = mock_find_label.call_args[0][1]
        assert "contains" in xpath
        assert "Email" in xpath


class TestSetValueById:
    @patch("robo_appian.components.InputUtils.ComponentUtils.findComponentById")
    def test_sets_value_by_id(self, mock_find):
        wait = make_wait()
        input_el = MagicMock()
        mock_find.return_value = input_el
        with patch("robo_appian.components.InputUtils.ActionChains"):
            InputUtils.setValueById(wait, "myInput", "test value")
        input_el.send_keys.assert_called_once_with("test value")
        mock_find.assert_called_once_with(wait, "myInput")


class TestSetValueByPlaceholderText:
    @patch("robo_appian.components.InputUtils.ComponentUtils.waitForComponentToBeVisibleByXpath")
    def test_sets_value_by_placeholder(self, mock_find):
        wait = make_wait()
        input_el = MagicMock()
        mock_find.return_value = input_el
        with patch("robo_appian.components.InputUtils.ActionChains"):
            InputUtils.setValueByPlaceholderText(wait, "Enter name", "Jane")
        input_el.send_keys.assert_called_once_with("Jane")

    @patch("robo_appian.components.InputUtils.ComponentUtils.waitForComponentToBeVisibleByXpath")
    def test_xpath_uses_placeholder_attribute(self, mock_find):
        wait = make_wait()
        mock_find.return_value = MagicMock()
        with patch("robo_appian.components.InputUtils.ActionChains"):
            InputUtils.setValueByPlaceholderText(wait, "Search here", "query")
        xpath = mock_find.call_args[0][1]
        assert "@placeholder" in xpath
        assert "Search here" in xpath
