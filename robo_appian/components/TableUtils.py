import re
from typing import Any

from robo_appian.utils.ComponentUtils import ComponentUtils

Page = Any
Locator = Any


class TableUtils:
    @staticmethod
    def __findColumnNumberByColumnName(tableObject: Locator, columnName: str) -> int:
        xpath = f'./thead/tr/th[@scope="col" and @abbr={ComponentUtils.xpath_literal(columnName)}]'
        component = tableObject.locator(f"xpath={xpath}").first
        component.wait_for(state="visible")

        return TableUtils.__findColumnNumberByHeader(component, columnName)

    @staticmethod
    def __findColumnNumberByHeader(component: Locator, columnName: str) -> int:
        class_string = component.get_attribute("class") or ""
        class_match = re.search(r"\bheadCell_(\d+)\b", class_string)
        if class_match:
            return int(class_match.group(1))

        id_value = component.get_attribute("id") or ""
        id_match = re.search(r"_(\d+)$", id_value)
        if id_match:
            return int(id_match.group(1))

        raise ValueError(
            f"Could not determine the column index for header '{columnName}'."
        )

    @staticmethod
    def __findRowByColumnNameAndRowNumber(
        page: Page, rowNumber: int, columnName: str
    ) -> Locator:
        column_literal = ComponentUtils.xpath_literal(columnName)
        xpath = (
            f'.//table[./thead/tr/th[@abbr={column_literal}]]/tbody/tr[@data-dnd-name="row {rowNumber + 1}" '
            f'and not(ancestor::*[@aria-hidden="true"])'
            f' and not(ancestor-or-self::*[contains(@class, "---hidden")])]'
        )
        row = ComponentUtils.waitForComponentToBeVisibleByXpath(page, xpath)
        return row

    @staticmethod
    def findComponentFromTableCell(page: Page, rowNumber: int, columnName: str):
        """Find a component within a table cell using column name and row number.

        Args:
            page: Playwright Page object.
            rowNumber: Zero-based row number.
            columnName: Column name matching the header's abbr attribute.

        Returns:
            Locator: The component element within the cell.

        Raises:
            ValueError: If column or row cannot be found.
        """
        return TableUtils.findComponentByColumnNameAndRowNumber(
            page, rowNumber, columnName
        )

    @staticmethod
    def selectRowFromTableByColumnNameAndRowNumber(
        page: Page, rowNumber: int, columnName: str
    ):
        """Click and select a table row by column name and row number.

        Args:
            page: Playwright Page object.
            rowNumber: Zero-based row number.
            columnName: Column name matching the header's abbr attribute.
        """
        row = TableUtils.__findRowByColumnNameAndRowNumber(page, rowNumber, columnName)
        ComponentUtils.click(page, row)

    @staticmethod
    def findComponentByColumnNameAndRowNumber(
        page: Page, rowNumber: int, columnName: str
    ):
        """Find a component within a specific table cell.

        Args:
            page: Playwright Page object.
            rowNumber: Zero-based row number.
            columnName: Column name matching the header's abbr attribute.

        Returns:
            Locator: The component element at the specified cell location.

        Raises:
            ValueError: If column or row cannot be found.
        """
        tableObject = TableUtils.findTableByColumnName(page, columnName)
        xpath = f'./thead/tr/th[@abbr={ComponentUtils.xpath_literal(columnName)} and not(ancestor::*[@aria-hidden="true"]) and not(ancestor-or-self::*[contains(@class, "---hidden")])]'
        column = ComponentUtils.findChildComponentByXpath(page, tableObject, xpath)
        columnNumber = TableUtils.__findColumnNumberByHeader(column, columnName)

        tableRow = TableUtils.__findRowByColumnNameAndRowNumber(
            page, rowNumber, columnName
        )
        child_xpath = f"./td[{columnNumber + 1}]/*"
        return ComponentUtils.findChildComponentByXpath(page, tableRow, child_xpath)

    @staticmethod
    def findTableByColumnName(page: Page, columnName: str):
        """Find a table by one of its column names.

        Args:
            page: Playwright Page object.
            columnName: Column name matching a header's abbr attribute.

        Returns:
            Locator: The table element.

        Raises:
            TimeoutError: If table with the specified column is not found.
        """
        xpath = (
            f".//table[./thead/tr/th[@abbr={ComponentUtils.xpath_literal(columnName)}]]"
        )
        return ComponentUtils.waitForComponentToBeVisibleByXpath(page, xpath)

    @staticmethod
    def rowCount(tableObject: Locator):
        """Get the number of visible rows in a table.

        Args:
            tableObject: Locator pointing to a table element.

        Returns:
            int: The count of visible data rows (excluding empty grid messages).
        """
        xpath = "./tbody/tr[./td[not (@data-empty-grid-message)]]"
        rows = tableObject.locator(f"xpath={xpath}")
        return rows.count()
