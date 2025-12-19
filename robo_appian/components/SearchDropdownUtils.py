from robo_appian.components.InputUtils import  InputUtils
from robo_appian.utils.ComponentUtils import ComponentUtils
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


class SearchDropdownUtils:
    """
    Utility class for interacting with search dropdown components in Appian UI.
    Usage Example:
        # Select a value from a search dropdown
        from robo_appian.components.SearchDropdownUtils import SearchDropdownUtils
        SearchDropdownUtils.selectSearchDropdownValueByLabelText(wait, "Status", "Approved")
    """

    @staticmethod
    def __selectSearchDropdownValueByDropdownId(
        wait: WebDriverWait, component_id: str, value: str
    ):
        if not component_id:
            raise ValueError("Invalid component_id provided.")

        input_component_id = str(component_id) + "_searchInput"
        try:
            wait.until(EC.presence_of_element_located((By.ID, input_component_id)))
            input_component = wait.until(
                EC.element_to_be_clickable((By.ID, input_component_id))
            )
        except Exception as e:
            raise Exception(
                f"Failed to locate or click input component with ID '{input_component_id}': {e}"
            ) from e
        InputUtils._setValueByComponent(wait, input_component, value)

        dropdown_option_id = str(component_id) + "_list"

        xpath = f'.//ul[@id="{dropdown_option_id}"]/li[./div[normalize-space(.)="{value}"]][1]'
        try:
            component = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        except Exception as e:
            raise Exception(
                f"Failed to locate or click dropdown option with XPath '{xpath}': {e}"
            ) from e 
         
        ComponentUtils.click(wait, component)

    @staticmethod
    def __selectSearchDropdownValueByPartialLabelText(
        wait: WebDriverWait, label: str, value: str
    ):
        xpath = f'.//div[./div/span[contains(normalize-space(.), "{label}")]]/div/div/div/div[@role="combobox" and not(@aria-disabled="true")]'
        try:
            combobox = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        except Exception as e:
            raise Exception(
                f"Failed to locate or click dropdown component with XPath '{xpath}': {e}"
            ) from e

        SearchDropdownUtils._selectSearchDropdownValueByComboboxComponent(
            wait, combobox, value
        )

    @staticmethod
    def __selectSearchDropdownValueByLabelText(
        wait: WebDriverWait, label: str, value: str
    ):
        xpath = f'.//div[./div/span[normalize-space(.)="{label}"]]/div/div/div/div[@role="combobox" and not(@aria-disabled="true")]'
        try:
            combobox = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        except Exception as e:
            raise Exception(
                f"Failed to locate or click dropdown component with XPath '{xpath}': {e}"
            ) from e
        SearchDropdownUtils._selectSearchDropdownValueByComboboxComponent(
            wait, combobox, value
        )

    @staticmethod
    def _selectSearchDropdownValueByComboboxComponent(
        wait: WebDriverWait, combobox: WebElement, value: str
    ):
        id = combobox.get_attribute("id")
        if id is not None:
            component_id = id.rsplit("_value", 1)[0]
        else:
            raise Exception("Combobox element does not have an 'id' attribute.")

        ComponentUtils.click(wait, combobox)

        SearchDropdownUtils.__selectSearchDropdownValueByDropdownId(
            wait, component_id, value
        )

    @staticmethod
    def selectSearchDropdownValueByLabelText(
        wait: WebDriverWait, dropdown_label: str, value: str
    ):
        """Selects a value from a search dropdown by label text.
        Args:
            wait (WebDriverWait): The WebDriverWait instance to use for waiting.
            dropdown_label (str): The label text of the dropdown.
            value (str): The value to select from the dropdown.
        """
        try:
            SearchDropdownUtils.__selectSearchDropdownValueByLabelText(
                wait, dropdown_label, value
            )
        except Exception as e:
            raise Exception(
                f"Failed to select value '{value}' from dropdown with label '{dropdown_label}': {e}"
            ) from e

    @staticmethod
    def selectSearchDropdownValueByPartialLabelText(
        wait: WebDriverWait, dropdown_label: str, value: str
    ):
        """Selects a value from a search dropdown by partial label text.
        Args:
            wait (WebDriverWait): The WebDriverWait instance to use for waiting.
            dropdown_label (str): The label text of the dropdown.
            value (str): The value to select from the dropdown.
        """
        SearchDropdownUtils.__selectSearchDropdownValueByPartialLabelText(
            wait, dropdown_label, value
        )
