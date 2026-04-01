import re

from playwright.sync_api import Locator, Page

from robo_appian.components.InputUtils import InputUtils
from robo_appian.utils.ComponentUtils import ComponentUtils


class SearchInputUtils:
    @staticmethod
    def __text_regex(text: str, exact: bool):
        normalized_text = ComponentUtils.validate_text_input(text, "text")
        parts = [re.escape(part) for part in normalized_text.split()]
        whitespace_pattern = r"[\s\u00A0]+"
        text_pattern = whitespace_pattern.join(parts)
        if exact:
            return re.compile(rf"^\s*{text_pattern}\s*$")
        return re.compile(text_pattern)

    @staticmethod
    def __normalize_text(text: str) -> str:
        normalized_text = ComponentUtils.validate_text_input(text, "text")
        return " ".join(normalized_text.replace("\u00A0", " ").split())

    @staticmethod
    def __wait_for_visible(locator: Locator) -> Locator:
        component = locator.first
        component.wait_for(state="visible")
        return component

    @staticmethod
    def __findSearchInputComponentByLabel(page: Page, label: str, exact: bool):
        normalized_label = ComponentUtils.validate_label_text(label)
        label_regex = SearchInputUtils.__text_regex(normalized_label, exact)

        try:
            return SearchInputUtils.__wait_for_visible(
                page.get_by_role("combobox", name=label_regex)
            )
        except Exception:
            pass

        container = (
            page.locator("div")
            .filter(has=page.locator("span").filter(has_text=label_regex))
            .filter(has=page.locator('[role="combobox"]'))
        )
        return SearchInputUtils.__wait_for_visible(
            container.locator('[role="combobox"]:visible')
        )

    @staticmethod
    def __findDropdownOption(dropdown: Locator, value: str) -> Locator:
        normalized_value = SearchInputUtils.__normalize_text(value)
        option_locators = dropdown.get_by_role("option")

        def find_matching_option(exact: bool):
            for index in range(option_locators.count()):
                option = option_locators.nth(index)
                if not option.is_visible():
                    continue

                option_text = SearchInputUtils.__normalize_text(option.inner_text())
                if exact and option_text == normalized_value:
                    return option
                if not exact and normalized_value in option_text:
                    return option
            return None

        exact_match = ComponentUtils.retry_until(
            lambda: find_matching_option(True),
            timeout_result=None,
        )
        if exact_match is not None:
            return exact_match

        partial_match = ComponentUtils.retry_until(
            lambda: find_matching_option(False),
            timeout_result=None,
        )
        if partial_match is not None:
            return partial_match

        raise ValueError(f"No dropdown option matched value: {normalized_value}")

    @staticmethod
    def __findSearchInputComponentsByLabelAndSelectValue(
        page: Page, label: str, value: str, exact: bool
    ):
        search_input_component = SearchInputUtils.__findSearchInputComponentByLabel(
            page, label, exact
        )
        dropdown_list_id = search_input_component.get_attribute("aria-controls")

        if not dropdown_list_id:
            raise ValueError(
                "Search input component does not have 'aria-controls' attribute."
            )

        InputUtils._setValueByComponent(page, search_input_component, value)

        dropdown = SearchInputUtils.__wait_for_visible(
            page.locator(f'ul[id="{dropdown_list_id}"][role="listbox"]:visible')
        )
        drop_down_item = SearchInputUtils.__findDropdownOption(dropdown, value)
        ComponentUtils.click(page, drop_down_item)
        return search_input_component

    @staticmethod
    def __selectSearchInputComponentsByPartialLabelText(
        page: Page, label: str, value: str
    ):
        return SearchInputUtils.__findSearchInputComponentsByLabelAndSelectValue(
            page, label, value, False
        )

    @staticmethod
    def __selectSearchInputComponentsByLabelText(page: Page, label: str, value: str):
        return SearchInputUtils.__findSearchInputComponentsByLabelAndSelectValue(
            page, label, value, True
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
