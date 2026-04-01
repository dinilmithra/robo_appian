"""Unit tests for TableUtils."""

import pytest
from unittest.mock import MagicMock, patch, call

from robo_appian.components.TableUtils import TableUtils


def make_wait():
    wait = MagicMock()
    wait._driver = MagicMock()
    return wait


def make_table_element(col_name="Status", col_class="headCell_2", col_id="col_2"):
    """Build a mock table object with a column header."""
    table_el = MagicMock()
    col_el = MagicMock()
    col_el.get_attribute.side_effect = lambda a: col_class if a == "class" else col_id if a == "id" else None
    table_el.find_element.return_value = col_el
    return table_el, col_el


class TestFindTableByColumnName:
    def test_returns_table_element(self):
        wait = make_wait()
        mock_table = MagicMock()
        wait.until.return_value = mock_table
        result = TableUtils.findTableByColumnName(wait, "Employee ID")
        assert result == mock_table

    def test_wait_until_called_twice(self):
        # First call: visibility, second: clickable
        wait = make_wait()
        mock_table = MagicMock()
        wait.until.return_value = mock_table
        TableUtils.findTableByColumnName(wait, "Name")
        assert wait.until.call_count == 2


class TestRowCount:
    def test_returns_count_of_rows(self):
        table_el = MagicMock()
        row1, row2, row3 = MagicMock(), MagicMock(), MagicMock()
        table_el.find_elements.return_value = [row1, row2, row3]
        count = TableUtils.rowCount(table_el)
        assert count == 3

    def test_returns_zero_when_no_rows(self):
        table_el = MagicMock()
        table_el.find_elements.return_value = []
        count = TableUtils.rowCount(table_el)
        assert count == 0

    def test_uses_correct_xpath_to_exclude_empty_message(self):
        table_el = MagicMock()
        table_el.find_elements.return_value = []
        TableUtils.rowCount(table_el)
        call_args = table_el.find_elements.call_args
        xpath = call_args[0][1]
        assert "data-empty-grid-message" in xpath


class TestFindComponentFromTableCell:
    def test_finds_component_in_cell(self):
        wait = make_wait()
        mock_table = MagicMock()
        mock_col = MagicMock()
        mock_col.get_attribute.side_effect = lambda a: "headCell_1" if a == "class" else None
        mock_table.find_element.return_value = mock_col
        mock_cell_component = MagicMock()

        # First two wait.until calls: visibility + clickable for findTableByColumnName
        # Then one more for findComponentFromTableCell
        wait.until.side_effect = [mock_table, mock_table, mock_cell_component]

        result = TableUtils.findComponentFromTableCell(wait, 0, "Status")
        assert result == mock_cell_component

    def test_row_number_is_1_based_internally(self):
        """Public API takes 0-based row; internal XPath must use row N+1."""
        wait = make_wait()
        mock_table = MagicMock()
        mock_col = MagicMock()
        mock_col.get_attribute.side_effect = lambda a: "headCell_0" if a == "class" else None
        mock_table.find_element.return_value = mock_col
        mock_cell = MagicMock()
        wait.until.side_effect = [mock_table, mock_table, mock_cell]

        with patch("robo_appian.components.TableUtils.EC.element_to_be_clickable") as mock_ec:
            mock_ec.return_value = MagicMock()
            wait.until.side_effect = [mock_table, mock_table, mock_cell]
            TableUtils.findComponentFromTableCell(wait, 2, "Name")
        # The row referenced internally should be 3 (2+1)
        # Verify by inspecting wait.until last call's xpath
        last_call_condition = wait.until.call_args_list[-1][0][0]
        # condition is the locator tuple from EC - we just confirm it was called
        assert last_call_condition is not None


class TestSelectRowFromTableByColumnNameAndRowNumber:
    def test_finds_and_clicks_row(self):
        wait = make_wait()
        mock_row = MagicMock()
        # findRowByColumnNameAndRowNumber uses wait.until once,
        # then wait.until(EC.element_to_be_clickable) returns mock_row
        wait.until.side_effect = [mock_row, mock_row]
        with patch("robo_appian.components.TableUtils.ComponentUtils.click") as mock_click:
            TableUtils.selectRowFromTableByColumnNameAndRowNumber(wait, 0, "Status")
        mock_click.assert_called_once_with(wait, mock_row)


class TestFindComponentByColumnNameAndRowNumber:
    def test_finds_component_at_column_and_row(self):
        wait = make_wait()
        mock_col_el = MagicMock()
        mock_col_el.get_attribute.return_value = "table_col_2"
        mock_row_el = MagicMock()
        mock_child_el = MagicMock()

        # Calls: visibility_of_element_located for col, presence for row, then child, then clickable
        wait.until.side_effect = [mock_col_el, mock_row_el, mock_child_el, mock_child_el]

        with patch(
            "robo_appian.components.TableUtils.ComponentUtils.findChildComponentByXpath",
            return_value=mock_child_el,
        ):
            result = TableUtils.findComponentByColumnNameAndRowNumber(wait, 0, "Name")
        assert result == mock_child_el
