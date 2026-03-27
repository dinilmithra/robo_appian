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
            f'and not(ancestor::*[@aria-hidden="true"])]'
        )
        row = ComponentUtils.waitForComponentToBeVisibleByXpath(page, xpath)
        return row

    @staticmethod
    def findComponentFromTableCell(page: Page, rowNumber: int, columnName: str):
        return TableUtils.findComponentByColumnNameAndRowNumber(
            page, rowNumber, columnName
        )

    @staticmethod
    def selectRowFromTableByColumnNameAndRowNumber(
        page: Page, rowNumber: int, columnName: str
    ):
        row = TableUtils.__findRowByColumnNameAndRowNumber(page, rowNumber, columnName)
        ComponentUtils.click(page, row)

    @staticmethod
    def findComponentByColumnNameAndRowNumber(
        page: Page, rowNumber: int, columnName: str
    ):
        tableObject = TableUtils.findTableByColumnName(page, columnName)
        xpath = f'./thead/tr/th[@abbr={ComponentUtils.xpath_literal(columnName)} and not(ancestor::*[@aria-hidden="true")] ]'
        column = ComponentUtils.findChildComponentByXpath(page, tableObject, xpath)
        columnNumber = TableUtils.__findColumnNumberByHeader(column, columnName)

        tableRow = TableUtils.__findRowByColumnNameAndRowNumber(
            page, rowNumber, columnName
        )
        child_xpath = f"./td[{columnNumber + 1}]/*"
        return ComponentUtils.findChildComponentByXpath(page, tableRow, child_xpath)

    @staticmethod
    def findTableByColumnName(page: Page, columnName: str):
        xpath = (
            f".//table[./thead/tr/th[@abbr={ComponentUtils.xpath_literal(columnName)}]]"
        )
        return ComponentUtils.waitForComponentToBeVisibleByXpath(page, xpath)

    @staticmethod
    def rowCount(tableObject: Locator):
        xpath = "./tbody/tr[./td[not (@data-empty-grid-message)]]"
        rows = tableObject.locator(f"xpath={xpath}")
        return rows.count()
