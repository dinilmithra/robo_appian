from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver


class TableUtils:
    """
    Utility class for interacting with table components in Appian UI.

        Usage Example:

        # Find a table using a column name
        from robo_appian.components.TableUtils import TableUtils
        table = TableUtils.findTableUsingColumnName(wait, "Status")

    """

    @staticmethod
    def findTableUsingColumnName(wait: WebDriverWait, columnName: str):
        """
        Finds a table component that contains a column with the specified name.

        Parameters:
            wait: Selenium WebDriverWait instance.
            columnName: The name of the column to search for in the table.

        Returns:
            The Selenium WebElement for the table component.

        Example:
            table = TableUtils.findTableUsingColumnName(wait, "Status")

        """
        # This method locates a table that contains a header cell with the specified column name.
        # It uses XPath to find the table element that has a header cell with the specified 'columnName'.
        # The 'abbr' attribute is used to match the column name, which is a common practice in Appian UI tables.

        # xpath = f".//table[./thead/tr/th[@abbr='{columnName}']]"
        xpath = f'.//table[./thead/tr/th[@abbr="{columnName}"]]'
        component = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        return component

    @staticmethod
    def clickOnLinkUsingHoverText(wait, columnName, rowNumber, hoverText):
        """
        Clicks on a link in a table cell identified by its column name, row number, and the hover text of the link.

        Parameters:
            wait: Selenium WebDriverWait instance.
            columnName: The name of the column where the link is located.
            rowNumber: The row number (0-based index) where the link is located.
            hoverText: The text that appears when hovering over the link.

        Example:
            TableUtils.clickOnLinkUsingHoverText(wait, "Status", 2, "View Details")

        """

        # This method locates a link within a specific table cell based on the column name and row number.
        # It constructs an XPath that targets the table cell containing the link with the specified hover text.
        # The XPath first identifies the table by the column name, then finds the specific row and cell,
        # and finally looks for the link with the specified hover text.

        xpath = f".//table[./thead/tr/th[@abbr='{columnName}']]/tbody/tr[@data-dnd-name='row {rowNumber + 1}']/td[not (@data-empty-grid-message)]/div/p/a[./span[text()='{hoverText}']]"
        # xpath=f".//table[./thead/tr/th/div[text()='{columnName}']][1]/tbody/tr[@data-dnd-name='row {rowNumber}']/td/div/p/a[./span[text()='{hoverText}']]"
        component = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        component.click()

    @staticmethod
    def clickOnButtonUsingHoverText(wait, columnName, rowNumber, hoverText):
        """
        Clicks on a button in a table cell identified by its column name, row number, and the hover text of the button.

        Parameters:
            wait: Selenium WebDriverWait instance.
            columnName: The name of the column where the button is located.
            rowNumber: The row number (0-based index) where the button is located.
            hoverText: The text that appears when hovering over the button.

        Example:
            TableUtils.clickOnButtonUsingHoverText(wait, "Actions", 2, "Delete")

        """
        # This method locates a button within a specific table cell based on the column name and row number.
        # It constructs an XPath that targets the table cell containing the button with the specified hover text.
        # The XPath first identifies the table by the column name, then finds the specific row and cell,
        # and finally looks for the button with the specified hover text.

        # TODO rowNumber = rowNumber + 1  # Adjusting for 1-based index in XPath

        xpath = f".//table[./thead/tr/th[@abbr='{columnName}']]/tbody/tr[@data-dnd-name='row {rowNumber}']/td[not (@data-empty-grid-message)]"
        component = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        component.click()

        xpath = f".//table[./thead/tr/th[@abbr='{columnName}']]/tbody/tr[@data-dnd-name='row {rowNumber}']/td[not (@data-empty-grid-message)]/div/div/button[./span[text()='{hoverText}']]"
        component = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        component.click()

    @staticmethod
    def rowCount(tableObject):
        """
        Returns the number of rows in a table, excluding empty grid messages.

        Parameters:
            tableObject: The Selenium WebElement representing the table.

        Returns:
            The number of rows in the table.

        Example:
            count = TableUtils.rowCount(table)

        """
        # This method counts the number of rows in a table by finding all the table row elements
        # that do not have the 'data-empty-grid-message' attribute.

        xpath = "./tbody/tr[./td[not (@data-empty-grid-message)]]"
        rows = tableObject.find_elements(By.XPATH, xpath)
        return len(rows)

    @staticmethod
    def findColumNumberUsingColumnName(tableObject, columnName):
        """
        Finds the column number in a table based on the column name.

        Parameters:
            tableObject: The Selenium WebElement representing the table.
            columnName: The name of the column to find.

        Returns:
            The index of the column (0-based).

        Example:
            column_number = TableUtils.findColumNumberUsingColumnName(table, "Status")

        """
        # This method locates the column header cell with the specified column name
        # and extracts the column index from its class attribute.

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
    def find_component_from_tabele_cell(wait, rowNumber, columnName):
        """
        Finds a component within a specific table cell based on the row number and column name.

        Parameters:
            wait: Selenium WebDriverWait instance.
            rowNumber: The row number (0-based index) where the component is located.
            columnName: The name of the column where the component is located.

        Returns:
            The Selenium WebElement for the component within the specified table cell.

        Example:
            component = TableUtils.find_component_from_tabele_cell(wait, 2, "Status")

        """
        # This method locates a specific component within a table cell based on the provided row number
        # and column name. It constructs an XPath that targets the table cell containing the specified column
        # and row, and then retrieves the component within that cell.

        tableObject = TableUtils.findTableUsingColumnName(wait, columnName)
        columnNumber = TableUtils.findColumNumberUsingColumnName(
            tableObject, columnName
        )
        # xpath=f'./tbody/tr[@data-dnd-name="row {rowNumber+1}"]/td[not (@data-empty-grid-message)][{columnNumber}]'
        # component = tableObject.find_elements(By.XPATH, xpath)
        rowNumber = rowNumber + 1
        columnNumber = columnNumber + 1
        xpath = f'.//table[./thead/tr/th[@abbr="{columnName}"]]/tbody/tr[@data-dnd-name="row {rowNumber}"]/td[not (@data-empty-grid-message)][{columnNumber}]/*'
        component = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        # childComponent=component.find_element(By.xpath("./*"))
        return component
