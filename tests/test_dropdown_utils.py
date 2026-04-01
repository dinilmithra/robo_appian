"""Unit tests for DropdownUtils."""

import pytest
import time
from unittest.mock import MagicMock, patch, call
from selenium.common.exceptions import NoSuchElementException

from robo_appian.components.DropdownUtils import DropdownUtils
from robo_appian.utils.ComponentUtils import ComponentUtils


def make_wait():
    wait = MagicMock()
    wait._driver = MagicMock()
    return wait


def make_combobox(component_id="combo-123", aria_controls="list-123"):
    el = MagicMock()

    def get_attr(name):
        return component_id if name == "id" else aria_controls if name == "aria-controls" else None

    el.get_attribute.side_effect = get_attr
    return el


class TestSelectDropdownValueByLabelText:
    @patch.object(ComponentUtils, "click")
    def test_selects_value_by_label(self, mock_click):
        wait = make_wait()
        combobox = make_combobox("c1", "list-1")
        option_el = MagicMock()
        # wait.until: 1) combobox, 2) element in __clickCombobox, 3) option
        wait.until.side_effect = [combobox, combobox, option_el]
        DropdownUtils.selectDropdownValueByLabelText(wait, "Status", "Active")
        option_el.click.assert_called_once()

    @patch.object(ComponentUtils, "click")
    def test_raises_value_error_when_no_aria_controls(self, mock_click):
        wait = make_wait()
        combobox = make_combobox("c1", None)
        # wait.until: 1) combobox, 2) element in __clickCombobox
        wait.until.side_effect = [combobox, combobox]
        with pytest.raises(ValueError, match="aria-controls"):
            DropdownUtils.selectDropdownValueByLabelText(wait, "Status", "Active")

    def test_raises_value_error_when_no_combobox_id(self):
        wait = make_wait()
        combobox = make_combobox(None, "list-1")
        wait.until.return_value = combobox
        with pytest.raises(ValueError, match="id"):
            DropdownUtils.selectDropdownValueByLabelText(wait, "Status", "Active")


class TestSelectDropdownValueByPartialLabelText:
    @patch.object(ComponentUtils, "click")
    def test_selects_value_by_partial_label(self, mock_click):
        wait = make_wait()
        combobox = make_combobox("c2", "list-2")
        option_el = MagicMock()
        wait.until.side_effect = [combobox, combobox, option_el]
        DropdownUtils.selectDropdownValueByPartialLabelText(wait, "Stat", "Active")
        option_el.click.assert_called_once()


class TestSelectDropdownValueByComboboxComponent:
    @patch.object(ComponentUtils, "click")
    def test_selects_value_via_combobox(self, mock_click):
        wait = make_wait()
        combobox = make_combobox("c3", "list-3")
        option_el = MagicMock()
        # wait.until: 1) element in __clickCombobox, 2) option
        wait.until.side_effect = [combobox, option_el]
        DropdownUtils.selectDropdownValueByComboboxComponent(wait, combobox, "Option A")
        option_el.click.assert_called_once()


class TestCheckReadOnlyStatusByLabelText:
    def test_returns_true_when_read_only_element_found(self):
        wait = make_wait()
        wait._driver.find_element.return_value = MagicMock()
        result = DropdownUtils.checkReadOnlyStatusByLabelText(wait, "Status")
        assert result is True

    def test_returns_false_when_element_not_found(self):
        wait = make_wait()
        wait._driver.find_element.side_effect = NoSuchElementException()
        result = DropdownUtils.checkReadOnlyStatusByLabelText(wait, "Status")
        assert result is False


class TestCheckEditableStatusByLabelText:
    def test_returns_true_when_editable(self):
        wait = make_wait()
        wait._driver.find_element.return_value = MagicMock()
        result = DropdownUtils.checkEditableStatusByLabelText(wait, "Status")
        assert result is True

    def test_returns_false_when_not_editable(self):
        wait = make_wait()
        wait._driver.find_element.side_effect = NoSuchElementException()
        result = DropdownUtils.checkEditableStatusByLabelText(wait, "Status")
        assert result is False


class TestWaitForDropdownToBeEnabled:
    @patch("robo_appian.components.DropdownUtils.time.sleep")
    def test_returns_true_when_enabled_immediately(self, mock_sleep):
        wait = make_wait()
        with patch.object(DropdownUtils, "checkEditableStatusByLabelText", return_value=True):
            result = DropdownUtils.waitForDropdownToBeEnabled(wait, "Status")
        assert result is True
        mock_sleep.assert_not_called()

    @patch("robo_appian.components.DropdownUtils.time.sleep")
    def test_returns_false_on_timeout(self, mock_sleep):
        wait = make_wait()
        with patch.object(
            DropdownUtils, "checkEditableStatusByLabelText", return_value=False
        ):
            result = DropdownUtils.waitForDropdownToBeEnabled(
                wait, "Status", wait_interval=0.5, timeout=1
            )
        assert result is False

    @patch("robo_appian.components.DropdownUtils.time.sleep")
    def test_returns_true_after_retry(self, mock_sleep):
        wait = make_wait()
        with patch.object(
            DropdownUtils,
            "checkEditableStatusByLabelText",
            side_effect=[False, True],
        ):
            result = DropdownUtils.waitForDropdownToBeEnabled(
                wait, "Status", wait_interval=0.5, timeout=2
            )
        assert result is True


class TestCheckDropdownOptionValueExists:
    @patch.object(ComponentUtils, "click")
    def test_returns_true_when_option_exists(self, mock_click):
        wait = make_wait()
        combobox = make_combobox("c4", "list-4")
        option_el = MagicMock()
        # wait.until: 1) combobox, 2) element in __clickCombobox, 3) option (found)
        wait.until.side_effect = [combobox, combobox, option_el]
        result = DropdownUtils.checkDropdownOptionValueExists(wait, "Status", "Active")
        assert result is True

    @patch.object(ComponentUtils, "click")
    def test_returns_false_when_option_missing(self, mock_click):
        wait = make_wait()
        combobox = make_combobox("c5", "list-5")
        # wait.until: 1) combobox, 2) element in __clickCombobox, 3) raises NoSuchElementException
        wait.until.side_effect = [combobox, combobox, NoSuchElementException()]
        result = DropdownUtils.checkDropdownOptionValueExists(wait, "Status", "Missing")
        assert result is False


class TestGetDropdownOptionValues:
    @patch.object(ComponentUtils, "click")
    def test_returns_list_of_option_texts(self, mock_click):
        wait = make_wait()
        combobox = make_combobox("c6", "list-6")
        opt1, opt2 = MagicMock(), MagicMock()
        opt1.text = "  Option A  "
        opt2.text = "Option B"
        option_elements = [opt1, opt2]
        # wait.until: 1) combobox, 2) element in __clickCombobox(open),
        # 3) option elements, 4) element in __clickCombobox(close)
        wait.until.side_effect = [combobox, combobox, option_elements, combobox]
        result = DropdownUtils.getDropdownOptionValues(wait, "Status")
        assert "Option A" in result
        assert "Option B" in result

    @patch.object(ComponentUtils, "click")
    def test_skips_empty_text_options(self, mock_click):
        wait = make_wait()
        combobox = make_combobox("c7", "list-7")
        opt_empty = MagicMock()
        opt_empty.text = "   "
        opt_real = MagicMock()
        opt_real.text = "Real Option"
        wait.until.side_effect = [combobox, combobox, [opt_empty, opt_real], combobox]
        result = DropdownUtils.getDropdownOptionValues(wait, "Status")
        assert "Real Option" in result
        assert "" not in result


class TestWaitForDropdownValuesToBeChanged:
    @patch("robo_appian.components.DropdownUtils.time.sleep")
    def test_breaks_when_values_change(self, mock_sleep):
        wait = make_wait()
        initial_values = ["A", "B"]
        new_values = ["A", "B", "C"]
        with patch.object(
            DropdownUtils, "getDropdownOptionValues", return_value=new_values
        ):
            DropdownUtils.waitForDropdownValuesToBeChanged(
                wait, "Status", initial_values, poll_frequency=0.5, timeout=2
            )
        mock_sleep.assert_not_called()

    @patch("robo_appian.components.DropdownUtils.time.sleep")
    def test_polls_until_timeout_when_unchanged(self, mock_sleep):
        wait = make_wait()
        initial = ["A"]
        with patch.object(
            DropdownUtils, "getDropdownOptionValues", return_value=["A"]
        ):
            DropdownUtils.waitForDropdownValuesToBeChanged(
                wait, "Status", initial, poll_frequency=0.5, timeout=1
            )
        mock_sleep.assert_called()
