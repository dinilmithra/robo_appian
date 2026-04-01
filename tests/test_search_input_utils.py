"""Unit tests for SearchInputUtils."""

import pytest
from unittest.mock import MagicMock, patch

from robo_appian.components.SearchInputUtils import SearchInputUtils


def make_wait():
    wait = MagicMock()
    wait._driver = MagicMock()
    return wait


class TestSelectSearchDropdownByLabelText:
    @patch("robo_appian.components.SearchInputUtils.ComponentUtils.waitForComponentToBeVisibleByXpath")
    @patch("robo_appian.components.SearchInputUtils.InputUtils._setValueByComponent")
    @patch("robo_appian.components.SearchInputUtils.ComponentUtils.click")
    def test_selects_value_by_label(self, mock_click, mock_set_value, mock_find):
        wait = make_wait()
        search_input = MagicMock()
        search_input.get_attribute.return_value = "dropdown-list-id"
        list_item = MagicMock()
        mock_find.side_effect = [search_input, list_item]
        SearchInputUtils.selectSearchDropdownByLabelText(wait, "Employee Name", "John Doe")
        mock_set_value.assert_called_once_with(wait, search_input, "John Doe")
        mock_click.assert_called_once_with(wait, list_item)

    @patch("robo_appian.components.SearchInputUtils.ComponentUtils.waitForComponentToBeVisibleByXpath")
    def test_raises_value_error_when_no_aria_controls(self, mock_find):
        wait = make_wait()
        search_input = MagicMock()
        search_input.get_attribute.return_value = None
        search_input.text = "Employee Name"
        mock_find.return_value = search_input
        with pytest.raises(ValueError, match="aria-controls"):
            SearchInputUtils.selectSearchDropdownByLabelText(wait, "Employee Name", "John")

    @patch("robo_appian.components.SearchInputUtils.ComponentUtils.waitForComponentToBeVisibleByXpath")
    @patch("robo_appian.components.SearchInputUtils.InputUtils._setValueByComponent")
    @patch("robo_appian.components.SearchInputUtils.ComponentUtils.click")
    def test_xpath_uses_exact_label(self, mock_click, mock_set_value, mock_find):
        wait = make_wait()
        search_input = MagicMock()
        search_input.get_attribute.return_value = "list-id"
        list_item = MagicMock()
        mock_find.side_effect = [search_input, list_item]
        SearchInputUtils.selectSearchDropdownByLabelText(wait, "Manager", "Bob")
        first_xpath = mock_find.call_args_list[0][0][1]
        assert "Manager" in first_xpath
        assert "combobox" in first_xpath


class TestSelectSearchDropdownByPartialLabelText:
    @patch("robo_appian.components.SearchInputUtils.ComponentUtils.waitForComponentToBeVisibleByXpath")
    def test_raises_on_missing_aria_controls(self, mock_find):
        wait = make_wait()
        search_input = MagicMock()
        search_input.get_attribute.return_value = None
        search_input.text = "Employee"
        mock_find.return_value = search_input
        with pytest.raises(ValueError, match="aria-controls"):
            SearchInputUtils.selectSearchDropdownByPartialLabelText(wait, "Emp", "Jane")
