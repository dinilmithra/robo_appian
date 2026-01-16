from selenium.webdriver.support.ui import WebDriverWait
from robo_appian.components.InputUtils import InputUtils
from robo_appian.utils.ComponentUtils import ComponentUtils


class SearchInputUtils:
    """
    Search and select from searchable input components in Appian UI.

    Similar to SearchDropdownUtils, but for input components that support filtering/search.
    Finds the input by label, types a search term, waits for matching options in a dropdown list,
    and selects the option.

    All methods follow the wait-first pattern: pass WebDriverWait as the first argument.

    Examples:
        >>> from robo_appian import SearchInputUtils
        >>> # Select by exact label match
        >>> SearchInputUtils.selectSearchDropdownByLabelText(wait, "Employee Name", "John Doe")
        >>> # Select by partial label match
        >>> SearchInputUtils.selectSearchDropdownByPartialLabelText(wait, "Employee", "John")

    Note:
        - Searchable inputs often appear in Appian forms for employee/user selection
        - Uses ARIA combobox and listbox patterns for element discovery
        - Waits for listbox options to populate after typing search term
    """

    @staticmethod
    def __findSearchInputComponentsByLabelPathAndSelectValue(
        wait: WebDriverWait, xpath: str, value: str
    ):

        search_input_component = ComponentUtils.waitForComponentToBeVisibleByXpath(
            wait, xpath
        )
        attribute: str = "aria-controls"
        dropdown_list_id = search_input_component.get_attribute(attribute)
        if dropdown_list_id:
            InputUtils._setValueByComponent(wait, search_input_component, value)
            xpath = f'.//ul[@id="{dropdown_list_id}" and @role="listbox" ]/li[@role="option" and @tabindex="-1" and ./div/div/div/div/div/div/p[normalize-space(.)="{value}"][1]]'
            drop_down_item = ComponentUtils.waitForComponentToBeVisibleByXpath(
                wait, xpath
            )
            ComponentUtils.click(wait, drop_down_item)
        else:
            raise ValueError(
                f"Search input component with label '{search_input_component.text}' does not have 'aria-controls' attribute."
            )

        return search_input_component

    @staticmethod
    def __selectSearchInputComponentsByPartialLabelText(
        wait: WebDriverWait, label: str, value: str
    ):
        xpath = f'.//div[./div/span[contains(normalize-space(.)="{label}"]]/div/div/div/input[@role="combobox"]'
        SearchInputUtils.__findSearchInputComponentsByLabelPathAndSelectValue(
            wait, xpath, value
        )

    @staticmethod
    def __selectSearchInputComponentsByLabelText(
        wait: WebDriverWait, label: str, value: str
    ):
        xpath = f'.//div[./div/span[normalize-space(translate(., "\u00a0", " "))="{label}"]]/div/div/div/input[@role="combobox"]'
        SearchInputUtils.__findSearchInputComponentsByLabelPathAndSelectValue(
            wait, xpath, value
        )

    @staticmethod
    def selectSearchDropdownByLabelText(wait: WebDriverWait, label: str, value: str):
        """
        Select a value from a search input using exact label match.

        Args:
            wait: WebDriverWait instance.
            label: Exact visible label text of the search input.
            value: Exact text of the option to select from the dropdown.

        Returns:
            None

        Examples:
            >>> SearchInputUtils.selectSearchDropdownByLabelText(wait, "Employee Name", "John Doe")
        """
        SearchInputUtils.__selectSearchInputComponentsByLabelText(wait, label, value)

    @staticmethod
    def selectSearchDropdownByPartialLabelText(
        wait: WebDriverWait, label: str, value: str
    ):
        """
        Select a value from a search input using partial label match.

        Args:
            wait: WebDriverWait instance.
            label: Partial visible label text (uses contains matching).
            value: Exact text of the option to select from the dropdown.

        Returns:
            None

        Examples:
            >>> SearchInputUtils.selectSearchDropdownByPartialLabelText(wait, "Employee", "John")
        """
        SearchInputUtils.__selectSearchInputComponentsByPartialLabelText(
            wait, label, value
        )
