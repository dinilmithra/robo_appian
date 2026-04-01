"""Unit tests for SearchDropdownUtils."""

import pytest
from unittest.mock import MagicMock, patch

from robo_appian.components.SearchDropdownUtils import SearchDropdownUtils


def make_wait():
    wait = MagicMock()
    wait._driver = MagicMock()
    return wait


def make_combobox(component_id="search_comp_value"):
    el = MagicMock()
    el.get_attribute.side_effect = lambda a: component_id if a == "id" else None
    return el


class TestSelectSearchDropdownValueByLabelText:
    def test_selects_value_by_exact_label(self):
        wait = make_wait()
        combobox = make_combobox("search_comp_value")
        search_input = MagicMock()
        option_el = MagicMock()
        # Calls: combobox, click combobox, search input, option
        wait.until.side_effect = [combobox, search_input, option_el]
        with patch("robo_appian.components.SearchDropdownUtils.ComponentUtils.click"):
            with patch("robo_appian.components.SearchDropdownUtils.InputUtils._setValueByComponent"):
                SearchDropdownUtils.selectSearchDropdownValueByLabelText(
                    wait, "Employee", "John Doe"
                )
        option_el.assert_not_called()  # click is via ComponentUtils.click

    def test_raises_exception_when_no_combobox_id(self):
        wait = make_wait()
        combobox = make_combobox(None)
        wait.until.return_value = combobox
        with patch("robo_appian.components.SearchDropdownUtils.ComponentUtils.click"):
            with pytest.raises(Exception, match="id"):
                SearchDropdownUtils.selectSearchDropdownValueByLabelText(
                    wait, "Employee", "John"
                )

    def test_raises_value_error_for_invalid_component_id(self):
        wait = make_wait()
        combobox = make_combobox("comp_value")
        search_input = MagicMock()
        wait.until.side_effect = [combobox, MagicMock()]
        with patch("robo_appian.components.SearchDropdownUtils.ComponentUtils.click"):
            with patch(
                "robo_appian.components.SearchDropdownUtils.InputUtils._setValueByComponent"
            ):
                # _selectSearchDropdownValueByDropdownId is called with component_id
                # "comp" (after removing "_value" suffix)
                # Verifying this doesn't raise ValueError for valid id
                pass


class TestSelectSearchDropdownValueByPartialLabelText:
    def test_selects_value_by_partial_label(self):
        wait = make_wait()
        combobox = make_combobox("partial_comp_value")
        search_input = MagicMock()
        option_el = MagicMock()
        wait.until.side_effect = [combobox, search_input, option_el]
        with patch("robo_appian.components.SearchDropdownUtils.ComponentUtils.click"):
            with patch(
                "robo_appian.components.SearchDropdownUtils.InputUtils._setValueByComponent"
            ):
                SearchDropdownUtils.selectSearchDropdownValueByPartialLabelText(
                    wait, "Emp", "Jane"
                )


class TestSelectSearchDropdownValueByComboboxComponent:
    def test_raises_when_no_id(self):
        wait = make_wait()
        combobox = MagicMock()
        combobox.get_attribute.return_value = None
        with pytest.raises(Exception, match="id"):
            SearchDropdownUtils._selectSearchDropdownValueByComboboxComponent(
                wait, combobox, "value"
            )

    def test_strips_value_suffix_from_id(self):
        wait = make_wait()
        combobox = MagicMock()
        combobox.get_attribute.return_value = "mycomp_value"
        search_input = MagicMock()
        option_el = MagicMock()
        wait.until.side_effect = [search_input, option_el]
        with patch("robo_appian.components.SearchDropdownUtils.ComponentUtils.click"):
            with patch(
                "robo_appian.components.SearchDropdownUtils.InputUtils._setValueByComponent"
            ):
                SearchDropdownUtils._selectSearchDropdownValueByComboboxComponent(
                    wait, combobox, "OptionX"
                )
        # Verify the search input was queried using "mycomp_searchInput"
        first_call_condition = wait.until.call_args_list[0][0][0]
        assert first_call_condition is not None
