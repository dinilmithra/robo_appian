from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement


class DropdownUtils:
    """
    Utility class for interacting with dropdown components in Appian UI.
    Usage Example:
        # Select a value from a dropdown
        from robo_appian.components.DropdownUtils import DropdownUtils
        DropdownUtils.selectDropdownValueByLabelText(wait, "Status", "Approved")
    """

    @staticmethod
    def __selectDropdownValueByDropdownOptionId(wait: WebDriverWait, dropdown_option_id: str, value: str):
        option_xpath = f'.//div/ul[@id="{dropdown_option_id}"]/li[./div[normalize-space(text())="{value}"]]'
        try:
            try:
                component = wait.until(EC.presence_of_element_located((By.XPATH, option_xpath)))
                component = wait.until(EC.element_to_be_clickable((By.XPATH, option_xpath)))
            except Exception as e:
                raise Exception(
                    f'Could not locate or click dropdown option "{value}" with dropdown option id "{dropdown_option_id}": {str(e)}'
                )
        except Exception as e:
            raise Exception(f'Could not find or click dropdown option "{value}" with xpath "{option_xpath}": {str(e)}')
        component.click()

    @staticmethod
    def __selectDropdownValueByPartialLabelText(wait: WebDriverWait, label: str, value: str):
        """
        Selects a value from a dropdown by its label text.

        :param wait: WebDriverWait instance to wait for elements.
        :param label: The label of the dropdown.
        :param value: The value to select from the dropdown.
        """

        xpath = f'.//div[./div/span[contains(normalize-space(text()), "{label}")]]/div/div/div/div[@role="combobox" and not(@aria-disabled="true")]'
        try:
            component = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        except Exception as e:
            raise Exception(f'Could not find or click dropdown with partial label "{label}" using xpath "{xpath}": {str(e)}')

        dropdown_option_id = component.get_attribute("aria-controls")
        if dropdown_option_id is None:
            raise Exception('Dropdown component does not have a valid "aria-controls" attribute.')
        component.click()

        DropdownUtils.__selectDropdownValueByDropdownOptionId(wait, dropdown_option_id, value)

    @staticmethod
    def __selectDropdownValueByLabelText(wait: WebDriverWait, label: str, value: str):
        """
        Selects a value from a dropdown by its label text.

        :param wait: WebDriverWait instance to wait for elements.
        :param label: The label of the dropdown.
        :param value: The value to select from the dropdown.
        """
        xpath = f'.//div[./div/span[normalize-space(text())="{label}"]]/div/div/div/div[@role="combobox" and not(@aria-disabled="true")]'
        try:
            component = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        except Exception as e:
            raise Exception(f'Could not find or click dropdown with label "{label}" using xpath "{xpath}": {str(e)}')

        dropdown_option_id = component.get_attribute("aria-controls")
        if dropdown_option_id is None:
            raise Exception('Dropdown component does not have a valid "aria-controls" attribute.')
        component.click()

        DropdownUtils.__selectDropdownValueByDropdownOptionId(wait, dropdown_option_id, value)

    @staticmethod
    def __selectDropdownValueByComboBoxId(wait: WebDriverWait, combo_box_Id: str, value: str):
        # component = wait.until(EC.element_to_be_clickable((By.ID, combo_box_Id)))
        xpath = f'.//div[@id="{combo_box_Id}" and @role="combobox" and not(@aria-disabled="true")]'
        try:
            component = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        except Exception as e:
            raise Exception(f'Could not find or click dropdown with combobox id "{combo_box_Id}" using xpath "{xpath}": {str(e)}')

        dropdown_option_id = component.get_attribute("aria-controls")
        if dropdown_option_id is None:
            raise Exception('Dropdown component does not have a valid "aria-controls" attribute.')
        component.click()

        DropdownUtils.__selectDropdownValueByDropdownOptionId(wait, dropdown_option_id, value)

    @staticmethod
    def __findComboboxIdByDropdownComponent(wait: WebDriverWait, component: WebElement):
        xpath = './div/div/div/div[@role="combobox"]'
        component = component.find_element(By.XPATH, xpath)
        id = component.get_attribute("id")
        if id is None:
            raise Exception('Dropdown component does not have a valid "id" attribute.')
        return id

    @staticmethod
    def selectDropdownValueByDropdownComponent(wait: WebDriverWait, component: WebElement, value: str):
        id = DropdownUtils.__findComboboxIdByDropdownComponent(wait, component)
        DropdownUtils.__selectDropdownValueByComboBoxId(wait, id, value)

    @staticmethod
    def selectDropdownValueByLabelText(wait: WebDriverWait, dropdown_label: str, value: str):
        DropdownUtils.__selectDropdownValueByLabelText(wait, dropdown_label, value)

    @staticmethod
    def selectDropdownValueByPartialLabelText(wait: WebDriverWait, dropdown_label: str, value: str):
        DropdownUtils.__selectDropdownValueByPartialLabelText(wait, dropdown_label, value)
