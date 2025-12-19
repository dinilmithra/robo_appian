import time
from robo_appian.utils.ComponentUtils import ComponentUtils
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
    def __findComboboxByLabelText(
        wait: WebDriverWait, label: str, isPartialText: bool = False
    ):
        """
        Finds the combobox element by its label text.
        :param wait: WebDriverWait instance to wait for elements.
        :param label: The label of the combobox.
        :param isPartialText: Whether to use partial text matching for the label.
        :return: The combobox WebElement.
        Example:
            combobox = DropdownUtils.__findComboboxByLabelText(wait, "Dropdown Label", isPartialText=False)
            combobox = DropdownUtils.__findComboboxByLabelText(wait, "Dropdown Label", isPartialText=True)
            combobox = DropdownUtils.__findComboboxByLabelText(wait, "Dropdown Label")
        """

        if isPartialText:
            xpath = f'//span[contains(normalize-space(.), "{label}")]/ancestor::div[@role="presentation"][1]//div[@aria-labelledby=//span[contains(normalize-space(.), "{label}")]/@id and @role="combobox" and not(@aria-disabled="true")]'
        else:
            xpath = f'//span[normalize-space(.)="{label}"]/ancestor::div[@role="presentation"][1]//div[@aria-labelledby=//span[normalize-space(.)="{label}"]/@id and @role="combobox" and not(@aria-disabled="true")]'

        try:
            component = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        except Exception as e:
            raise Exception(f'Could not find combobox with label "{label}" ') from e

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
        try:
            id = combobox.get_attribute("id")
            element = wait.until(EC.element_to_be_clickable((By.ID, id)))
            ComponentUtils.click(wait, element)

        except Exception as e:
            raise Exception(f"Could not click combobox") from e

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
            raise Exception(
                f'Could not find dropdown option "{value}" with dropdown option id "{dropdown_option_id}"'
            ) from e

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
            DropdownUtils.selectDropdownValueByDropdownOptionId(wait, "dropdown_option_id", "Option Value")
        """
        option_xpath = f'.//div/ul[@id="{dropdown_option_id}"]/li[./div[normalize-space(.)="{value}"]]'
        try:
            try:
                component = wait.until(
                    EC.presence_of_element_located((By.XPATH, option_xpath))
                )
                component = wait.until(
                    EC.element_to_be_clickable((By.XPATH, option_xpath))
                )
                component.click()
            except Exception as e:
                raise Exception(
                    f'Could not locate or click dropdown option "{value}" with dropdown option id "{dropdown_option_id}"'  # noqa: E501
                ) from e
        except Exception as e:
            raise Exception(
                f'Could not find or click dropdown option "{value}" with xpath "{option_xpath}"'
            ) from e

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
        # xpath = f'.//div[./div/span[normalize-space(.)="{label}"]]/div/div/p[normalize-space(translate(., "\u00a0", " "))]'
        xpath = f'//span[normalize-space(.)="{label}"]/ancestor::div[@role="presentation"][1]//div[@aria-labelledby=//span[normalize-space(.)="{label}"]/@id and not(@role="combobox")]'
        try:
            wait._driver.find_element(By.XPATH, xpath)
            return True
        except NoSuchElementException:
            return False
        except Exception as e:
            raise Exception(
                f'Error checking read-only status for label "{label}"'
            ) from e

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
            raise Exception(
                f'Error checking editable status for label "{label}"'
            ) from e

    @staticmethod
    def waitForDropdownToBeEnabled(
        wait: WebDriverWait, label: str, wait_interval: float = 0.5, timeout: int = 2
    ):
        elapsed_time = 0
        status = False

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
            raise Exception(
                f'Could not get dropdown option values for label "{dropdown_label}"'
            ) from e

    @staticmethod
    def waitForDropdownValuesToBeChanged(
        wait: WebDriverWait,
        dropdown_label: str,
        initial_values: list[str],
        poll_frequency: float = 0.5,
        timeout: int = 2,
    ):

        elapsed_time = 0
        poll_frequency = 0.5
        timeout = 4  # seconds
        while elapsed_time < timeout:

            current_values: list[str] = DropdownUtils.getDropdownOptionValues(
                wait, dropdown_label
            )

            # Compare job series values before and after position job title selection
            if initial_values != current_values:
                break
            time.sleep(poll_frequency)
            elapsed_time += poll_frequency
