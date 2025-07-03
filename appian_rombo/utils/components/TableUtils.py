from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class TableUtils():

    @staticmethod
    def findTableUsingColumnName(wait, columnName):
        # xpath = f".//table[./thead/tr/th[@abbr='{columnName}']]"
        xpath = f'.//table[./thead/tr/th[@abbr="{columnName}"]]'
        component = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        return component

    @staticmethod
    def clickOnLinkUsingHoverText(wait, columnName, rowNumber, hoverText):
        xpath = f".//table[./thead/tr/th[@abbr='{columnName}']]/tbody/tr[@data-dnd-name='row {rowNumber + 1}']/td[not (@data-empty-grid-message)]/div/p/a[./span[text()='{hoverText}']]"
        # xpath=f".//table[./thead/tr/th/div[text()='{columnName}']][1]/tbody/tr[@data-dnd-name='row {rowNumber}']/td/div/p/a[./span[text()='{hoverText}']]"       
        component = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        component.click()

    @staticmethod
    def clickOnButtonUsingHoverText(wait, columnName, rowNumber, hoverText):
        xpath = f".//table[./thead/tr/th[@abbr='{columnName}']]/tbody/tr[@data-dnd-name='row {rowNumber}']/td[not (@data-empty-grid-message)]"
        component = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        component.click()

        xpath = f".//table[./thead/tr/th[@abbr='{columnName}']]/tbody/tr[@data-dnd-name='row {rowNumber}']/td[not (@data-empty-grid-message)]/div/div/button[./span[text()='{hoverText}']]"
        component = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        component.click()

    @staticmethod
    def rowCount(tableObject):
        xpath = "./tbody/tr[./td[not (@data-empty-grid-message)]]"
        rows = tableObject.find_elements(By.XPATH, xpath)
        return len(rows)

    @staticmethod
    def findColumNumberUsingColumnName(tableObject, columnName):

        xpath = f'./thead/tr/th[@scope="col" and @abbr="{columnName}"]'
        component = tableObject.find_element(By.XPATH, xpath)
        class_string = component.get_attribute("class")
        partial_string = "headCell_"
        words = class_string.split()
        selected_word = None

        for word in words:
            if partial_string in word:
                selected_word = word

        data = selected_word.split("_")
        return int(data[1])

    @staticmethod
    def find_component_from_tabele_cell(wait, rowNumber, columnName):

        tableObject = TableUtils.findTableUsingColumnName(wait, columnName)
        columnNumber = TableUtils.findColumNumberUsingColumnName(tableObject, columnName)
        # xpath=f'./tbody/tr[@data-dnd-name="row {rowNumber+1}"]/td[not (@data-empty-grid-message)][{columnNumber}]'
        # component = tableObject.find_elements(By.XPATH, xpath)
        rowNumber = rowNumber + 1
        columnNumber = columnNumber + 1
        xpath = f'.//table[./thead/tr/th[@abbr="{columnName}"]]/tbody/tr[@data-dnd-name="row {rowNumber}"]/td[not (@data-empty-grid-message)][{columnNumber}]/*'
        component = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        # childComponent=component.find_element(By.xpath("./*"))
        return component
