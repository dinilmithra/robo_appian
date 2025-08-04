from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from robo_appian.components.InputUtils import InputUtils


class SearchDropdownUtils:
    """
    Utility class for interacting with search dropdown components in Appian UI.
    Usage Example:
        # Select a value from a search dropdown
        from robo_appian.components.SearchDropdownUtils import SearchDropdownUtils
        SearchDropdownUtils.selectSearchDropdownValueByLabelText(wait, "Status", "Approved")
    """

    @staticmethod
    def __selectSearchDropdownValueByDropdownOptionId(wait, component_id, dropdown_option_id, value):
        input_component_id = str(component_id) + "_searchInput"
        try:
            input_component = wait.until(EC.element_to_be_clickable((By.ID, input_component_id)))
        except Exception as e:
            raise RuntimeError(f"Failed to locate or click input component with ID '{input_component_id}': {e}")
        InputUtils._setValueByComponent(input_component, value)

        xpath = f'.//ul[@id="{dropdown_option_id}"]/li[./div[normalize-space(text())="{value}"]][1]'
        try:
            component = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        except Exception as e:
            raise RuntimeError(f"Failed to locate or click dropdown option with XPath '{xpath}': {e}")
        component.click()

    @staticmethod
    def __selectSearchDropdownValueByPartialLabelText(wait: WebDriverWait, label: str, value: str):
        xpath = f'.//div[./div/span[contains(normalize-space(text()), "{label}")]]/div/div/div/div[@role="combobox" and not(@aria-disabled="true")]'
        try:
            component = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        except Exception as e:
            raise RuntimeError(f"Failed to locate or click dropdown component with XPath '{xpath}': {e}")
        component_id = component.get_attribute("aria-labelledby")
        dropdown_id = component.get_attribute("aria-controls")
        component.click()

        SearchDropdownUtils.__selectSearchDropdownValueByDropdownOptionId(wait, component_id, dropdown_id, value)

    @staticmethod
    def __selectSearchDropdownValueByLabelText(wait: WebDriverWait, label: str, value: str):
        xpath = f'.//div[./div/span[normalize-space(text())="{label}"]]/div/div/div/div[@role="combobox" and not(@aria-disabled="true")]'
        try:
            component = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        except Exception as e:
            raise RuntimeError(f"Failed to locate or click dropdown component with XPath '{xpath}': {e}")
        component_id = component.get_attribute("aria-labelledby")
        dropdown_option_id = component.get_attribute("aria-controls")
        component.click()
        SearchDropdownUtils.__selectSearchDropdownValueByDropdownOptionId(wait, component_id, dropdown_option_id, value)

    @staticmethod
    def selectSearchDropdownValueByLabelText(wait: WebDriverWait, dropdown_label: str, value: str):
        """Selects a value from a search dropdown by label text.
        Args:
            wait (WebDriverWait): The WebDriverWait instance to use for waiting.
            dropdown_label (str): The label text of the dropdown.
            value (str): The value to select from the dropdown.
        """
        SearchDropdownUtils.__selectSearchDropdownValueByLabelText(wait, dropdown_label, value)

    @staticmethod
    def selectSearchDropdownValueByPartialLabelText(wait: WebDriverWait, dropdown_label: str, value: str):
        """Selects a value from a search dropdown by partial label text.
        Args:
            wait (WebDriverWait): The WebDriverWait instance to use for waiting.
            dropdown_label (str): The label text of the dropdown.
            value (str): The value to select from the dropdown.
        """
        SearchDropdownUtils.__selectSearchDropdownValueByPartialLabelText(wait, dropdown_label, value)
