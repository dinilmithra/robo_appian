from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException


class DropdownUtils:
    """
    Utility class for interacting with dropdown components in Appian UI.
    Usage Example:
        # Select a value from a dropdown
        from robo_appian.components.DropdownUtils import DropdownUtils
        DropdownUtils.selectDropdownValueByLabelText(wait, "Status", "Approved")
    """

    @staticmethod
    def __findComboboxByPartialLabelText(wait: WebDriverWait, label: str):
        """
        Finds a combobox by its partial label text.

        :param wait: Selenium WebDriverWait instance.
        :param label: The partial label of the combobox to find.
        :return: WebElement representing the combobox.
        Example:
            component = DropdownUtils.__findComboboxByPartialLabelText(wait, "Dropdown Label")
        """
        xpath = f'.//div[./div/span[contains(normalize-space(.), "{label}")]]/div/div/div/div[@role="combobox" and not(@aria-disabled="true")]'  # noqa: E501
        try:
            component = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        except Exception as e:
            raise Exception(f'Could not find combobox with partial label "{label}" : {str(e)}')

        return component

    @staticmethod
    def __findComboboxByLabelText(wait: WebDriverWait, label: str):
        """
        Finds a combobox by its label text.

        :param wait: Selenium WebDriverWait instance.
        :param label: The label of the combobox to find.
        :return: WebElement representing the combobox.
        Example:
            component = DropdownUtils.__findComboboxByLabelText(wait, "Dropdown Label")
        """
        xpath = f'.//div[./div/span[normalize-space(.)="{label}"]]/div/div/div/div[@role="combobox" and not(@aria-disabled="true")]'  # noqa: E501
        try:
            component = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        except Exception as e:
            raise Exception(f'Could not find combobox with label "{label}" : {str(e)}')

        return component

    @staticmethod
    def __clickCombobox(wait: WebDriverWait, combobox: WebElement):
        """
        Clicks the combobox to open the dropdown options.

        :param wait: WebDriverWait instance to wait for elements.
        :param combobox: The combobox WebElement.
        Example:
            DropdownUtils.__clickCombobox(wait, combobox)
        """
        combobox.click()

    @staticmethod
    def __findDropdownOptionId(wait: WebDriverWait, combobox: WebElement):
        """
        Finds the dropdown option id from the combobox.

        :param wait: WebDriverWait instance to wait for elements.
        :param combobox: The combobox WebElement.
        :return: The id of the dropdown options list.
        Example:
            dropdown_option_id = DropdownUtils.__findDropdownOptionId(wait, combobox)
        """
        dropdown_option_id = combobox.get_attribute("aria-controls")
        if dropdown_option_id is None:
            raise Exception('Dropdown component does not have a valid "aria-controls" attribute.')
        return dropdown_option_id

    @staticmethod
    def __checkDropdownOptionValueExistsByDropdownOptionId(wait: WebDriverWait, dropdown_option_id: str, value: str):
        """
        Checks if a dropdown option value exists by its option id and value.

        :param wait: WebDriverWait instance to wait for elements.
        :param dropdown_option_id: The id of the dropdown options list.
        :param value: The value to check in the dropdown.
        Example:
            exists = DropdownUtils.checkDropdownOptionValueExistsByDropdownOptionId(wait, "dropdown_option_id", "Option Value")
            if exists:
                print("The value exists in the dropdown.")
            else:
                print("The value does not exist in the dropdown.")
        """

        xpath = f'.//div/ul[@id="{dropdown_option_id}"]/li[./div[normalize-space(.)="{value}"]]'
        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            return True
        except NoSuchElementException:
            return False
        except Exception as e:
            raise Exception(f'Could not find dropdown option "{value}" with dropdown option id "{dropdown_option_id}": {str(e)}')

    @staticmethod
    def __selectDropdownValueByDropdownOptionId(wait: WebDriverWait, dropdown_option_id: str, value: str):
        """
        Selects a value from a dropdown by its option id and value.

        :param wait: WebDriverWait instance to wait for elements.
        :param dropdown_option_id: The id of the dropdown options list.
        :param value: The value to select from the dropdown.
        Example:
            DropdownUtils.selectDropdownValueByDropdownOptionId(wait, "dropdown_option_id", "Option Value")
        """
        option_xpath = f'.//div/ul[@id="{dropdown_option_id}"]/li[./div[normalize-space(.)="{value}"]]'
        try:
            try:
                component = wait.until(EC.presence_of_element_located((By.XPATH, option_xpath)))
                component = wait.until(EC.element_to_be_clickable((By.XPATH, option_xpath)))
            except Exception as e:
                raise Exception(
                    f'Could not locate or click dropdown option "{value}" with dropdown option id "{dropdown_option_id}": {str(e)}'  # noqa: E501
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
        combobox = DropdownUtils.__findComboboxByPartialLabelText(wait, label)
        DropdownUtils.__clickCombobox(wait, combobox)
        dropdown_option_id = DropdownUtils.__findDropdownOptionId(wait, combobox)
        DropdownUtils.__selectDropdownValueByDropdownOptionId(wait, dropdown_option_id, value)

    @staticmethod
    def __selectDropdownValueByLabelText(wait: WebDriverWait, label: str, value: str):
        """
        Selects a value from a dropdown by its label text.

        :param wait: WebDriverWait instance to wait for elements.
        :param label: The label of the dropdown.
        :param value: The value to select from the dropdown.
        """
        combobox = DropdownUtils.__findComboboxByLabelText(wait, label)
        DropdownUtils.__clickCombobox(wait, combobox)
        dropdown_option_id = DropdownUtils.__findDropdownOptionId(wait, combobox)
        DropdownUtils.__selectDropdownValueByDropdownOptionId(wait, dropdown_option_id, value)

    @staticmethod
    def checkReadOnlyStatusByLabelText(wait: WebDriverWait, label: str):
        """
        Checks if a dropdown is read-only by its label text.

        :param wait: WebDriverWait instance to wait for elements.
        :param label: The label of the dropdown.
        :return: True if the dropdown is read-only, False otherwise.
        Example:
            is_read_only = DropdownUtils.checkReadOnlyStatusByLabelText(wait, "Dropdown Label")
            if is_read_only:
                print("The dropdown is read-only.")
            else:
                print("The dropdown is editable.")
        """
        xpath = f'.//div[./div/span[normalize-space(.)="{label}"]]/div/div/p[text()]'
        try:
            wait._driver.find_element(By.XPATH, xpath)
            return True
        except NoSuchElementException:
            return False
        except Exception:
            raise Exception(f'Error checking read-only status for label "{label}"')

    @staticmethod
    def selectDropdownValueByComboboxComponent(wait: WebDriverWait, combobox: WebElement, value: str):
        """
        Selects a value from a dropdown using the combobox component.

        :param wait: WebDriverWait instance to wait for elements.
        :param combobox: The combobox WebElement.
        :param value: The value to select from the dropdown.
        Example:
            DropdownUtils.selectDropdownValueByComboboxComponent(wait, combobox, "Option Value")
        """
        dropdown_option_id = DropdownUtils.__findDropdownOptionId(wait, combobox)
        DropdownUtils.__clickCombobox(wait, combobox)
        DropdownUtils.__selectDropdownValueByDropdownOptionId(wait, dropdown_option_id, value)

    @staticmethod
    def selectDropdownValueByLabelText(wait: WebDriverWait, dropdown_label: str, value: str):
        """
        Selects a value from a dropdown by its label text.

        :param wait: WebDriverWait instance to wait for elements.
        :param dropdown_label: The label of the dropdown.
        :param value: The value to select from the dropdown.
        Example:
            DropdownUtils.selectDropdownValueByLabelText(wait, "Dropdown Label", "Option Value")
        """
        DropdownUtils.__selectDropdownValueByLabelText(wait, dropdown_label, value)

    @staticmethod
    def selectDropdownValueByPartialLabelText(wait: WebDriverWait, dropdown_label: str, value: str):
        """
        Selects a value from a dropdown by its partial label text.

        :param wait: WebDriverWait instance to wait for elements.
        :param dropdown_label: The partial label of the dropdown.
        :param value: The value to select from the dropdown.
        Example:
            DropdownUtils.selectDropdownValueByPartialLabelText(wait, "Dropdown Label", "Option Value")
        """
        DropdownUtils.__selectDropdownValueByPartialLabelText(wait, dropdown_label, value)

    @staticmethod
    def checkDropdownOptionValueExists(wait: WebDriverWait, dropdown_label: str, value: str):
        """
        Checks if a dropdown option value exists by its label text.

        :param wait: WebDriverWait instance to wait for elements.
        :param dropdown_label: The label of the dropdown.
        :param value: The value to check in the dropdown.
        :return: True if the value exists, False otherwise.
        Example:
            exists = DropdownUtils.checkDropdownOptionValueExists(wait, "Dropdown Label", "Option Value")
            if exists:
                print("The value exists in the dropdown.")
            else:
                print("The value does not exist in the dropdown.")
        """
        combobox = DropdownUtils.__findComboboxByLabelText(wait, dropdown_label)
        DropdownUtils.__clickCombobox(wait, combobox)
        dropdown_option_id = DropdownUtils.__findDropdownOptionId(wait, combobox)
        return DropdownUtils.__checkDropdownOptionValueExistsByDropdownOptionId(wait, dropdown_option_id, value)
