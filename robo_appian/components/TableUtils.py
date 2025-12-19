from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from robo_appian.utils.ComponentUtils import ComponentUtils


class TableUtils:
    """
    Utility class for handling table operations in Selenium WebDriver.
    Example usage:
        from selenium import webdriver
        from selenium.webdriver.support.ui import WebDriverWait
        from robo_appian.components.TableUtils import TableUtils

        driver = webdriver.Chrome()
        wait = WebDriverWait(driver, 10)
        table = TableUtils.findTableByColumnName(wait, "Status")
        row_count = TableUtils.rowCount(table)
        component = TableUtils.findComponentFromTableCell(wait, 1, "Status")
        driver.quit()

    """

    @staticmethod
    def rowCount(tableObject):
        """
        Counts the number of rows in a table.

        :param tableObject: The Selenium WebElement representing the table.
        :return: The number of rows in the table.
        Example:
            row_count = TableUtils.rowCount(table)
        """

        xpath = "./tbody/tr[./td[not (@data-empty-grid-message)]]"
        try:
            rows = tableObject.find_elements(By.XPATH, xpath)
        except Exception as e:
            raise Exception(f"Could not count rows in table: ") from e
        return len(rows)

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
            raise ValueError(f"Could not find a column with abbr '{columnName}' in the table header.")

        class_string = component.get_attribute("class")
        partial_string = "headCell_"
        words = class_string.split()
        selected_word = None

        for word in words:
            if partial_string in word:
                selected_word = word

        if selected_word is None:
            raise ValueError(f"Could not find a class containing '{partial_string}' in the column header for '{columnName}'.")

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
        try:
            component = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        except Exception as e:
            raise Exception(f"Could not find component in cell at row {rowNumber}, column '{columnName}': ") from e
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

        tableRow = TableUtils.__findRowByColumnNameAndRowNumber(wait, rowNumber, columnName)
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
        try:
            component = wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
        except Exception as e:
            raise Exception(f"Could not find table with column name '{columnName}': ") from e

        try:
            component = wait.until(EC.element_to_be_clickable(component))
        except Exception as e:
            raise Exception(f"Table found by column name '{columnName}' is not clickable: ") from e
        return component
