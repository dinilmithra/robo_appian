import time
from robo_appian.utils.ComponentUtils import ComponentUtils
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException


class DropdownUtils:
    """
    Utility class for interacting with dropdown components in a web application.
    Provides methods to select values, check statuses, and retrieve options from dropdowns.
    Example:
        DropdownUtils.selectDropdownValueByLabelText(wait, "Dropdown Label", "Option Value")
    """

    @staticmethod
    def __findComboboxByLabelText(
        wait: WebDriverWait, label: str, isPartialText: bool = False
    ):
        """
        Finds the combobox element by its label text.
        :param wait: WebDriverWait instance to wait for elements.
        :param label: The label of the dropdown.
        :param isPartialText: Whether to use partial text matching for the label.
        :return: The combobox WebElement.
        Example:
            combobox = DropdownUtils.__findComboboxByLabelText(wait, "Dropdown Label")
            combobox = DropdownUtils.__findComboboxByLabelText(wait, "Dropdown Label", isPartialText=True)
        """

        if isPartialText:
            xpath = f'//span[contains(normalize-space(.), "{label}")]/ancestor::div[@role="presentation"][1]//div[@role="combobox" and not(@aria-disabled="true")]'
        else:
            xpath = f'//span[text()="{label}"]/ancestor::div[@role="presentation"][1]//div[@role="combobox" and not(@aria-disabled="true")]'

        return wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))

    @staticmethod
    def __clickCombobox(wait: WebDriverWait, combobox: WebElement):
        """
        Clicks the combobox to open the dropdown options.

        :param wait: WebDriverWait instance to wait for elements.
        :param combobox: The combobox WebElement.
        Example:
            DropdownUtils.__clickCombobox(wait, combobox)
        """
        component_id = combobox.get_attribute("id")
        if not component_id:
            raise ValueError("Combobox element does not have an 'id' attribute.")
        element = wait.until(EC.element_to_be_clickable((By.ID, component_id)))
        ComponentUtils.click(wait, element)

    @staticmethod
    def __findDropdownOptionId(combobox: WebElement):
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
            raise Exception(
                'Dropdown component does not have a valid "aria-controls" attribute.'
            )
        return dropdown_option_id

    @staticmethod
    def __checkDropdownOptionValueExistsByDropdownOptionId(
        wait: WebDriverWait, dropdown_option_id: str, value: str
    ):
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
            raise

    @staticmethod
    def __selectDropdownValueByDropdownOptionId(
        wait: WebDriverWait, dropdown_option_id: str, value: str
    ):
        """
        Selects a value from a dropdown by its option id and value.
        :param wait: WebDriverWait instance to wait for elements.
        :param dropdown_option_id: The id of the dropdown options list.
        :param value: The value to select from the dropdown.
        Example:
            DropdownUtils.__selectDropdownValueByDropdownOptionId(wait, "dropdown_option_id", "Option Value")
        """
        option_xpath = f'.//div/ul[@id="{dropdown_option_id}"]/li[./div[normalize-space(.)="{value}"]]'
        component = wait.until(EC.element_to_be_clickable((By.XPATH, option_xpath)))
        component.click()

    @staticmethod
    def __selectDropdownValueByPartialLabelText(
        wait: WebDriverWait, label: str, value: str
    ):
        """
        Selects a value from a dropdown by its label text.

        :param wait: WebDriverWait instance to wait for elements.
        :param label: The label of the dropdown.
        :param value: The value to select from the dropdown.
        """
        combobox = DropdownUtils.__findComboboxByLabelText(wait, label, True)
        DropdownUtils.__clickCombobox(wait, combobox)
        dropdown_option_id = DropdownUtils.__findDropdownOptionId(combobox)
        DropdownUtils.__selectDropdownValueByDropdownOptionId(
            wait, dropdown_option_id, value
        )

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
        dropdown_option_id = DropdownUtils.__findDropdownOptionId(combobox)
        DropdownUtils.__selectDropdownValueByDropdownOptionId(
            wait, dropdown_option_id, value
        )

    @staticmethod
    def checkReadOnlyStatusByLabelText(wait: WebDriverWait, label: str):
        """
        Checks if a dropdown is read-only (disabled) by its label text.
        :param wait: WebDriverWait instance to wait for elements.
        :param label: The label of the dropdown.
        :return: True if the dropdown is read-only, False if editable.
        Example:
            is_readonly = DropdownUtils.checkReadOnlyStatusByLabelText(wait, "Dropdown Label")
            if is_readonly:
                print("The dropdown is read-only.")
            else:
                print("The dropdown is editable.")
        """
        # xpath = f'.//div[./div/span[normalize-space(.)="{label}"]]/div/div/p[normalize-space(translate(., "\u00a0", " "))]'
        xpath = f'//span[normalize-space(.)="{label}"]/ancestor::div[@role="presentation"][1]//div[@aria-labelledby=//span[normalize-space(.)="{label}"]/@id and not(@role="combobox")]'
        try:
            wait._driver.find_element(By.XPATH, xpath)
            return True
        except NoSuchElementException:
            return False
        except Exception as e:
            raise

    @staticmethod
    def checkEditableStatusByLabelText(wait: WebDriverWait, label: str):
        """
        Checks if a dropdown is editable (not disabled) by its label text.

        :param wait: WebDriverWait instance to wait for elements.
        :param label: The label of the dropdown.
        :return: True if the dropdown is editable, False if disabled.
        Example:
            is_editable = DropdownUtils.checkEditableStatusByLabelText(wait, "Dropdown Label")
            if is_editable:
                print("The dropdown is editable.")
            else:
                print("The dropdown is disabled.")
        """
        xpath = f'//span[normalize-space(translate(., "\u00a0", " "))="{label}"]/ancestor::div[@role="presentation"][1]//div[@aria-labelledby=//span[normalize-space(.)="{label}"]/@id and @role="combobox" and not(@aria-disabled="true")]'
        try:
            wait._driver.find_element(By.XPATH, xpath)
            return True  # If disabled element is found, dropdown is not editable
        except NoSuchElementException:
            return False  # If disabled element is not found, dropdown is editable
        except Exception as e:
            raise

    @staticmethod
    def waitForDropdownToBeEnabled(
        wait: WebDriverWait, label: str, wait_interval: float = 0.5, timeout: int = 2
    ):
        """
        Waits for a dropdown to become enabled (editable) by its label text.
        :param wait: WebDriverWait instance to wait for elements.
        :param label: The label of the dropdown.
        :param wait_interval: The interval (in seconds) to wait between checks.
        :param timeout: The maximum time (in seconds) to wait for the dropdown to become enabled.
        :return: True if the dropdown becomes enabled within the timeout, False otherwise.
        Example:
            is_enabled = DropdownUtils.waitForDropdownToBeEnabled(wait, "Dropdown Label")
            if is_enabled:
                print("The dropdown is enabled.")
            else:
                print("The dropdown is still disabled.")
        """
        elapsed_time = 0

        while elapsed_time < timeout:
            status = DropdownUtils.checkEditableStatusByLabelText(wait, label)
            if status:
                return True
            time.sleep(wait_interval)
            elapsed_time += wait_interval
        return False

    @staticmethod
    def selectDropdownValueByComboboxComponent(
        wait: WebDriverWait, combobox: WebElement, value: str
    ):
        """
        Selects a value from a dropdown using the combobox component.

        :param wait: WebDriverWait instance to wait for elements.
        :param combobox: The combobox WebElement.
        :param value: The value to select from the dropdown.
        Example:
            DropdownUtils.selectDropdownValueByComboboxComponent(wait, combobox, "Option Value")
        """
        dropdown_option_id = DropdownUtils.__findDropdownOptionId(combobox)
        DropdownUtils.__clickCombobox(wait, combobox)
        DropdownUtils.__selectDropdownValueByDropdownOptionId(
            wait, dropdown_option_id, value
        )

    @staticmethod
    def selectDropdownValueByLabelText(
        wait: WebDriverWait, dropdown_label: str, value: str
    ):
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
    def selectDropdownValueByPartialLabelText(
        wait: WebDriverWait, dropdown_label: str, value: str
    ):
        """
        Selects a value from a dropdown by its partial label text.

        :param wait: WebDriverWait instance to wait for elements.
        :param dropdown_label: The partial label of the dropdown.
        :param value: The value to select from the dropdown.
        Example:
            DropdownUtils.selectDropdownValueByPartialLabelText(wait, "Dropdown Label", "Option Value")
        """
        DropdownUtils.__selectDropdownValueByPartialLabelText(
            wait, dropdown_label, value
        )

    @staticmethod
    def checkDropdownOptionValueExists(
        wait: WebDriverWait, dropdown_label: str, value: str
    ):
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
        dropdown_option_id = DropdownUtils.__findDropdownOptionId(combobox)
        return DropdownUtils.__checkDropdownOptionValueExistsByDropdownOptionId(
            wait, dropdown_option_id, value
        )

    @staticmethod
    def getDropdownOptionValues(wait: WebDriverWait, dropdown_label: str) -> list[str]:
        """
        Gets all option values from a dropdown by its label text.

        :param wait: WebDriverWait instance to wait for elements.
        :param dropdown_label: The label of the dropdown.
        :return: A list of all option values in the dropdown.
        Example:
            values = DropdownUtils.getDropdownOptionValues(wait, "Dropdown Label")
        """
        combobox = DropdownUtils.__findComboboxByLabelText(wait, dropdown_label)
        DropdownUtils.__clickCombobox(wait, combobox)
        dropdown_option_id = DropdownUtils.__findDropdownOptionId(combobox)

        # Get all option elements
        xpath = f'//ul[@id="{dropdown_option_id}"]//li[@role="option"]/div'
        try:
            option_elements = wait.until(
                EC.presence_of_all_elements_located((By.XPATH, xpath))
            )
            # Extract text immediately to avoid stale element reference
            option_texts = []
            for element in option_elements:
                try:
                    text = element.text.strip()
                    if text:
                        option_texts.append(text)
                except Exception:
                    # If element becomes stale, try to re-find it
                    continue

            # If we got no texts due to stale elements, try one more time
            if not option_texts:
                option_elements = wait._driver.find_elements(By.XPATH, xpath)
                for element in option_elements:
                    try:
                        text = element.text.strip()
                        if text:
                            option_texts.append(text)
                    except Exception:
                        continue

            DropdownUtils.__clickCombobox(wait, combobox)
            return option_texts
        except Exception as e:
            raise

    @staticmethod
    def waitForDropdownValuesToBeChanged(
        wait: WebDriverWait,
        dropdown_label: str,
        initial_values: list[str],
        poll_frequency: float = 0.5,
        timeout: int = 2,
    ):
        """
        Waits for the values of a dropdown to change from the initial values.

        :param wait: WebDriverWait instance to wait for elements.
        :param dropdown_label: The label of the dropdown.
        :param initial_values: The initial values of the dropdown.
        :param poll_frequency: The interval (in seconds) to wait between checks.
        :param timeout: The maximum time (in seconds) to wait for the dropdown values to change.
        :return: True if the dropdown values change within the timeout, False otherwise.
        Example:
            initial_values = DropdownUtils.getDropdownOptionValues(wait, "Dropdown Label")
            is_changed = DropdownUtils.waitForDropdownValuesToBeChanged(wait, "Dropdown Label", initial_values)
            if is_changed:
                print("The dropdown values have changed.")
            else:
                print("The dropdown values have not changed within the timeout.")
        """

        elapsed_time = 0
        while elapsed_time < timeout:

            current_values: list[str] = DropdownUtils.getDropdownOptionValues(
                wait, dropdown_label
            )

            # Compare job series values before and after position job title selection
            if initial_values != current_values:
                break
            time.sleep(poll_frequency)
            elapsed_time += poll_frequency
