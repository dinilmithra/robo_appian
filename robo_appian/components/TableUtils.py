from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from robo_appian.utils.ComponentUtils import ComponentUtils


class TableUtils:
    """
    Interact with Appian grid/table components: read cells, click rows, find elements.

    Query and interact with table rows and cells using column names as locators.
    Automatically handles row/column indexing, finding cells by their position, and
    interacting with components within cells (buttons, links, inputs).

    Key concepts:
        - Columns are identified by their header 'abbr' (abbreviation) attribute
        - Rows are 0-based in public APIs (first row = 0)
        - Rows are internally 1-indexed in Appian's data-dnd-name (conversion is automatic)

    All methods follow the wait-first pattern: pass WebDriverWait as the first argument.

    Examples:
        >>> from robo_appian.components.TableUtils import TableUtils
        >>> from selenium.webdriver.support.ui import WebDriverWait

        # Find a table by column name and count rows
        table = TableUtils.findTableByColumnName(wait, "Employee ID")
        row_count = TableUtils.rowCount(table)
        print(f"Table has {row_count} rows")

        # Find and click component in specific cell (row 0, column "Status")
        TableUtils.selectRowFromTableByColumnNameAndRowNumber(wait, 0, "Employee ID")

        # Get a specific cell component
        edit_button = TableUtils.findComponentFromTableCell(wait, 0, "Actions")

        # Interact with element in table cell
        component = TableUtils.findComponentByColumnNameAndRowNumber(wait, 1, "Status")

    Note:
        - Tables are located by column header 'abbr' attribute
        - Column positions are derived from header class attributes (e.g., "headCell_2")
        - Hidden/aria-hidden elements are automatically excluded
    """

    @staticmethod
    def __findColumNumberByColumnName(tableObject, columnName):
        """
        Finds the column number in a table by its column name.

        :param tableObject: The Selenium WebElement representing the table.
        :param columnName: The name of the column to search for.
        :return: The index of the column (0-based).
        Example:
            column_number = TableUtils.__findColumNumberByColumnName(table, "Status")
        """

        xpath = f'./thead/tr/th[@scope="col" and @abbr="{columnName}"]'
        component = tableObject.find_element(By.XPATH, xpath)

        if component is None:
            raise ValueError(
                f"Could not find a column with abbr '{columnName}' in the table header."
            )

        class_string = component.get_attribute("class")
        partial_string = "headCell_"
        words = class_string.split()
        selected_word = None

        for word in words:
            if partial_string in word:
                selected_word = word

        if selected_word is None:
            raise ValueError(
                f"Could not find a class containing '{partial_string}' in the column header for '{columnName}'."
            )

        data = selected_word.split("_")
        return int(data[1])

    @staticmethod
    def __findRowByColumnNameAndRowNumber(wait, rowNumber, columnName):
        # xpath = f'.//table[./thead/tr/th/div[normalize-space(.)="{columnName}"] ]/tbody/tr[@data-dnd-name="row {rowNumber + 1}"]'
        xpath = f'.//table[./thead/tr/th[@abbr="{columnName}"]]/tbody/tr[@data-dnd-name="row {rowNumber + 1}" and not(ancestor::*[@aria-hidden="true"])]'
        row = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        return row

    @staticmethod
    def findComponentFromTableCell(wait, rowNumber, columnName):
        """
        Finds a component within a specific cell of a table by row number and column name.

        :param wait: Selenium WebDriverWait instance.
        :param rowNumber: The row number (0-based index).
        :param columnName: The name of the column to search in.
        :return: WebElement representing the component in the specified cell.
        Example:
            component = TableUtils.findComponentFromTableCell(wait, 1, "Status")
        """

        tableObject = TableUtils.findTableByColumnName(wait, columnName)
        columnNumber = TableUtils.__findColumNumberByColumnName(tableObject, columnName)
        rowNumber = rowNumber + 1
        columnNumber = columnNumber + 1
        xpath = f'.//table[./thead/tr/th[@abbr="{columnName}"]]/tbody/tr[@data-dnd-name="row {rowNumber}"]/td[not (@data-empty-grid-message)][{columnNumber}]/*'
        component = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        return component

    @staticmethod
    def selectRowFromTableByColumnNameAndRowNumber(wait, rowNumber, columnName):
        row = TableUtils.__findRowByColumnNameAndRowNumber(wait, rowNumber, columnName)
        row = wait.until(EC.element_to_be_clickable(row))
        ComponentUtils.click(wait, row)

    @staticmethod
    def findComponentByColumnNameAndRowNumber(wait, rowNumber, columnName):
        # xpath = f'.//table/thead/tr/th[./div[normalize-space(.)="{columnName}"]]'
        xpath = f'.//table/thead/tr/th[@abbr="{columnName}" and not(ancestor::*[@aria-hidden="true"]) ]'
        column = wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
        id = column.get_attribute("id")
        parts = id.rsplit("_", 1)
        columnNumber = int(parts[-1])

        tableRow = TableUtils.__findRowByColumnNameAndRowNumber(
            wait, rowNumber, columnName
        )
        xpath = f"./td[{columnNumber + 1}]/*"
        component = ComponentUtils.findChildComponentByXpath(wait, tableRow, xpath)
        component = wait.until(EC.element_to_be_clickable(component))
        return component

    @staticmethod
    def findTableByColumnName(wait: WebDriverWait, columnName: str):
        """
        Finds a table component by its column name.

        :param wait: Selenium WebDriverWait instance.
        :param columnName: The name of the column to search for.
        :return: WebElement representing the table.
        Example:
            component = TableUtils.findTableByColumnName(wait, "Status")
        """

        xpath = f'.//table[./thead/tr/th[@abbr="{columnName}"]]'
        component = wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))

        component = wait.until(EC.element_to_be_clickable(component))
        return component

    @staticmethod
    def rowCount(tableObject):
        """
        Count non-empty rows in a table.

        Returns the number of data rows (excluding empty grid message placeholders).

        Args:
            tableObject: WebElement representing the table (from findTableByColumnName).

        Returns:
            int: Number of rows in the table.

        Examples:
            >>> table = TableUtils.findTableByColumnName(wait, "Name")
            >>> rows = TableUtils.rowCount(table)
            >>> print(f"Found {rows} employees")
        """

        xpath = "./tbody/tr[./td[not (@data-empty-grid-message)]]"
        rows = tableObject.find_elements(By.XPATH, xpath)
        return len(rows)
