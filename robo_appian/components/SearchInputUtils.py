from playwright.sync_api import Page

from robo_appian.components.InputUtils import InputUtils
from robo_appian.utils.ComponentUtils import ComponentUtils


class SearchInputUtils:
    @staticmethod
    def __findSearchInputComponentsByLabelPathAndSelectValue(
        page: Page, xpath: str, value: str
    ):
        search_input_component = ComponentUtils.waitForComponentToBeVisibleByXpath(
            page, xpath
        )
        dropdown_list_id = search_input_component.get_attribute("aria-controls")

        if not dropdown_list_id:
            raise ValueError(
                "Search input component does not have 'aria-controls' attribute."
            )

        InputUtils._setValueByComponent(page, search_input_component, value)

        value_literal = ComponentUtils.xpath_literal(value)
        # Complex nested XPath for finding search option:
        # .//ul[@id=...] - Find the listbox container by aria-controls ID
        # /li[@role="option" and @tabindex="-1"] - Find inactive option items
        # and ./div/div/div/div/div/div/p[...] - Navigate deeply nested divs to text content
        # normalize-space(translate(...)) - Normalize NBSP characters and whitespace
        option_xpath = (
            f'.//ul[@id={ComponentUtils.xpath_literal(dropdown_list_id)} and @role="listbox"]'
            f"/li[@role=\"option\" and @tabindex=\"-1\" and ./div/div/div/div/div/div/p[normalize-space(translate(., '\u00a0', ' '))={value_literal}][1]]"
        )
        drop_down_item = ComponentUtils.waitForComponentToBeVisibleByXpath(
            page, option_xpath
        )
        ComponentUtils.click(page, drop_down_item)
        return search_input_component

    @staticmethod
    def __selectSearchInputComponentsByPartialLabelText(
        page: Page, label: str, value: str
    ):
        label_literal = ComponentUtils.xpath_literal(label)
        xpath = (
            ".//div[./div/span[contains(normalize-space(translate(., '\u00a0', ' ')), "
            f'{label_literal})]]/div/div/div/input[@role="combobox"]'
        )
        return SearchInputUtils.__findSearchInputComponentsByLabelPathAndSelectValue(
            page, xpath, value
        )

    @staticmethod
    def __selectSearchInputComponentsByLabelText(page: Page, label: str, value: str):
        label_literal = ComponentUtils.xpath_literal(label)
        xpath = (
            ".//div[./div/span[normalize-space(translate(., '\u00a0', ' '))="
            f'{label_literal}]]/div/div/div/input[@role="combobox"]'
        )
        return SearchInputUtils.__findSearchInputComponentsByLabelPathAndSelectValue(
            page, xpath, value
        )

    @staticmethod
    def selectSearchInputByLabelText(page: Page, label: str, value: str):
        """Select a value in a search input by exact label text.

        Args:
            page: Playwright Page object.
            label: Exact text to match in the search input label.
            value: The option value to search and select.

        Returns:
            Locator: The search input component that was filled.

        Raises:
            TimeoutError: If search input or option is not found.
        """
        return SearchInputUtils.__selectSearchInputComponentsByLabelText(
            page, label, value
        )

    @staticmethod
    def selectSearchInputByPartialLabelText(page: Page, label: str, value: str):
        """Select a value in a search input by partial label text match.

        Args:
            page: Playwright Page object.
            label: Partial text to match in the search input label.
            value: The option value to search and select.

        Returns:
            Locator: The search input component that was filled.

        Raises:
            TimeoutError: If search input or option is not found.
        """
        return SearchInputUtils.__selectSearchInputComponentsByPartialLabelText(
            page, label, value
        )

    @staticmethod
    def selectSearchDropdownByLabelText(page: Page, label: str, value: str):
        """Select a value in a search dropdown by exact label text.

        Args:
            page: Playwright Page object.
            label: Exact text to match in the search dropdown label.
            value: The option value to search and select.

        Returns:
            Locator: The search input component that was filled.
        """
        return SearchInputUtils.selectSearchInputByLabelText(page, label, value)

    @staticmethod
    def selectSearchDropdownByPartialLabelText(page: Page, label: str, value: str):
        """Select a value in a search dropdown by partial label text match.

        Args:
            page: Playwright Page object.
            label: Partial text to match in the search dropdown label.
            value: The option value to search and select.

        Returns:
            Locator: The search input component that was filled.
        """
        return SearchInputUtils.selectSearchInputByPartialLabelText(page, label, value)
