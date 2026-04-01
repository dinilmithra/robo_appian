"""Unit tests for ComponentDriver."""

import pytest
from unittest.mock import MagicMock, patch

from robo_appian.controllers.ComponentDriver import ComponentDriver


def make_wait():
    wait = MagicMock()
    wait._driver = MagicMock()
    return wait


class TestDateRouting:
    @patch("robo_appian.controllers.ComponentDriver.DateUtils.setValueByLabelText")
    def test_date_set_value(self, mock_fn):
        wait = make_wait()
        ComponentDriver.execute(wait, "Date", "Set Value", "Start Date", "01/01/2024")
        mock_fn.assert_called_once_with(wait, "Start Date", "01/01/2024")

    def test_date_unsupported_action_raises(self):
        wait = make_wait()
        with pytest.raises(ValueError, match="Unsupported action"):
            ComponentDriver.execute(wait, "Date", "Click", "Start Date", None)


class TestInputTextRouting:
    @patch("robo_appian.controllers.ComponentDriver.InputUtils.setValueByLabelText")
    def test_input_text_set_value(self, mock_fn):
        wait = make_wait()
        ComponentDriver.execute(wait, "Input Text", "Set Value", "Username", "john")
        mock_fn.assert_called_once_with(wait, "Username", "john")

    def test_input_text_unsupported_action_raises(self):
        wait = make_wait()
        with pytest.raises(ValueError, match="Unsupported action"):
            ComponentDriver.execute(wait, "Input Text", "Click", "Username", None)


class TestButtonRouting:
    @patch("robo_appian.controllers.ComponentDriver.ButtonUtils.clickByLabelText")
    def test_button_click(self, mock_fn):
        wait = make_wait()
        ComponentDriver.execute(wait, "Button", "Click", "Submit", None)
        mock_fn.assert_called_once_with(wait, "Submit")

    def test_button_unsupported_action_raises(self):
        wait = make_wait()
        with pytest.raises(ValueError, match="Unsupported action"):
            ComponentDriver.execute(wait, "Button", "Set Value", "Submit", "x")


class TestDropDownRouting:
    @patch("robo_appian.controllers.ComponentDriver.DropdownUtils.selectDropdownValueByLabelText")
    def test_dropdown_select(self, mock_fn):
        wait = make_wait()
        ComponentDriver.execute(wait, "Drop Down", "Select", "Status", "Active")
        mock_fn.assert_called_once_with(wait, "Status", "Active")

    def test_dropdown_unsupported_action_raises(self):
        wait = make_wait()
        with pytest.raises(ValueError, match="Unsupported action"):
            ComponentDriver.execute(wait, "Drop Down", "Click", "Status", None)


class TestSearchInputTextRouting:
    @patch("robo_appian.controllers.ComponentDriver.SearchInputUtils.selectSearchDropdownByLabelText")
    def test_search_input_select(self, mock_fn):
        wait = make_wait()
        ComponentDriver.execute(wait, "Search Input Text", "Select", "Employee", "John")
        mock_fn.assert_called_once_with(wait, "Employee", "John")

    def test_search_input_unsupported_action_raises(self):
        wait = make_wait()
        with pytest.raises(ValueError, match="Unsupported action"):
            ComponentDriver.execute(wait, "Search Input Text", "Click", "Employee", None)


class TestSearchDropDownRouting:
    @patch(
        "robo_appian.controllers.ComponentDriver.SearchDropdownUtils.selectSearchDropdownValueByLabelText"
    )
    def test_search_dropdown_select(self, mock_fn):
        wait = make_wait()
        ComponentDriver.execute(wait, "Search Drop Down", "Select", "Manager", "Alice")
        mock_fn.assert_called_once_with(wait, "Manager", "Alice")

    def test_search_dropdown_unsupported_action_raises(self):
        wait = make_wait()
        with pytest.raises(ValueError, match="Unsupported action"):
            ComponentDriver.execute(wait, "Search Drop Down", "Click", "Manager", None)


class TestLabelRouting:
    @patch("robo_appian.controllers.ComponentDriver.LabelUtils.isLabelExists")
    def test_label_find(self, mock_fn):
        wait = make_wait()
        ComponentDriver.execute(wait, "Label", "Find", "Success!", None)
        mock_fn.assert_called_once_with(wait, "Success!")

    def test_label_unsupported_action_raises(self):
        wait = make_wait()
        with pytest.raises(ValueError, match="Unsupported action"):
            ComponentDriver.execute(wait, "Label", "Click", "Success!", None)


class TestLinkRouting:
    @patch("robo_appian.controllers.ComponentDriver.LinkUtils.click")
    def test_link_click(self, mock_fn):
        wait = make_wait()
        ComponentDriver.execute(wait, "Link", "Click", "Learn More", None)
        mock_fn.assert_called_once_with(wait, "Learn More")

    def test_link_unsupported_action_raises(self):
        wait = make_wait()
        with pytest.raises(ValueError, match="Unsupported action"):
            ComponentDriver.execute(wait, "Link", "Set Value", "Learn More", "x")


class TestTabRouting:
    @patch("robo_appian.controllers.ComponentDriver.TabUtils.selectTabByLabelText")
    def test_tab_find_routes_to_select(self, mock_fn):
        wait = make_wait()
        ComponentDriver.execute(wait, "Tab", "Find", "Details", None)
        mock_fn.assert_called_once_with(wait, "Details")

    def test_tab_unsupported_action_raises(self):
        wait = make_wait()
        with pytest.raises(ValueError, match="Unsupported action"):
            ComponentDriver.execute(wait, "Tab", "Click", "Details", None)


class TestUnsupportedComponentType:
    def test_unsupported_type_raises_value_error(self):
        wait = make_wait()
        with pytest.raises(ValueError, match="Unsupported component type"):
            ComponentDriver.execute(wait, "Unknown Widget", "Click", "label", None)

    def test_empty_type_raises_value_error(self):
        wait = make_wait()
        with pytest.raises(ValueError, match="Unsupported component type"):
            ComponentDriver.execute(wait, "", "Click", "label", None)
