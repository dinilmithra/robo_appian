from robo_appian.components.InputUtils import InputUtils
from robo_appian.utils.ComponentUtils import ComponentUtils
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


class SearchDropdownUtils:
    """
    Select values from search-enabled dropdowns in Appian UI.

    Search dropdowns allow users to type to filter options, then click to select. These differ
    from standard dropdowns because they include a search/filter input field. Automatically
    types the search term, waits for options to populate, and clicks the matching option.

    All methods follow the wait-first pattern: pass WebDriverWait as the first argument.

    Examples:
        >>> from robo_appian import SearchDropdownUtils
        >>> # Select by exact label match
        >>> SearchDropdownUtils.selectSearchDropdownValueByLabelText(wait, "Employee", "John Doe")
        >>> # Select by partial label match
        >>> SearchDropdownUtils.selectSearchDropdownValueByPartialLabelText(wait, "Status", "Approved")

    Note:
        - Search dropdowns use the combobox ARIA pattern with ID-based suffixes (`_searchInput`, `_list`)
        - Component lookup by label is more reliable than searching by ID directly
        - Automatically waits for dropdown options to appear after typing search term
    """

    @staticmethod
    def __selectSearchDropdownValueByDropdownId(
        wait: WebDriverWait, component_id: str, value: str
    ):
        if not component_id:
            raise ValueError("Invalid component_id provided.")

        input_component_id = str(component_id) + "_searchInput"
        input_component = wait.until(
            EC.element_to_be_clickable((By.ID, input_component_id))
        )
        InputUtils._setValueByComponent(wait, input_component, value)

        dropdown_option_id = str(component_id) + "_list"

        xpath = f'.//ul[@id="{dropdown_option_id}"]/li[./div[normalize-space(.)="{value}"]][1]'
        component = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        ComponentUtils.click(wait, component)

    @staticmethod
    def __selectSearchDropdownValueByPartialLabelText(
        wait: WebDriverWait, label: str, value: str
    ):
        xpath = f'.//div[./div/span[contains(normalize-space(.), "{label}")]]/div/div/div/div[@role="combobox" and not(@aria-disabled="true")]'
        combobox = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))

        SearchDropdownUtils._selectSearchDropdownValueByComboboxComponent(
            wait, combobox, value
        )

    @staticmethod
    def __selectSearchDropdownValueByLabelText(
        wait: WebDriverWait, label: str, value: str
    ):
        xpath = f'.//div[./div/span[normalize-space(.)="{label}"]]/div/div/div/div[@role="combobox" and not(@aria-disabled="true")]'
        combobox = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
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
        """
        Select a value from a search dropdown using exact label match.

        Types the value into the search field, waits for filtered options to appear,
        then clicks the matching option.

        Args:
            wait: WebDriverWait instance.
            dropdown_label: Exact visible label text of the dropdown (e.g., "Employee").
            value: Exact text of the option to select (e.g., "John Doe").

        Returns:
            None

        Raises:
            TimeoutException: If dropdown or option not found within timeout.
            ValueError: If dropdown ID cannot be extracted from element.

        Examples:
            >>> SearchDropdownUtils.selectSearchDropdownValueByLabelText(wait, "Employee", "John Doe")
            >>> SearchDropdownUtils.selectSearchDropdownValueByLabelText(wait, "Status", "Approved")
        """
        SearchDropdownUtils.__selectSearchDropdownValueByLabelText(
            wait, dropdown_label, value
        )

    @staticmethod
    def selectSearchDropdownValueByPartialLabelText(
        wait: WebDriverWait, dropdown_label: str, value: str
    ):
        """
        Select a value from a search dropdown using partial label match.

        Useful when the dropdown label contains dynamic text (e.g., includes a count or suffix).
        Searches for the label using a contains check instead of exact match.

        Args:
            wait: WebDriverWait instance.
            dropdown_label: Partial visible label text (uses contains matching).
            value: Exact text of the option to select.

        Returns:
            None

        Raises:
            TimeoutException: If dropdown or option not found within timeout.
            ValueError: If dropdown ID cannot be extracted from element.

        Examples:
            >>> SearchDropdownUtils.selectSearchDropdownValueByPartialLabelText(wait, "Employee", "John")
        """
        SearchDropdownUtils.__selectSearchDropdownValueByPartialLabelText(
            wait, dropdown_label, value
        )
