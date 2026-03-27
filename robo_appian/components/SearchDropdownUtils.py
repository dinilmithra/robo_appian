from typing import Any

from robo_appian.components.InputUtils import InputUtils
from robo_appian.utils.ComponentUtils import ComponentUtils

Page = Any
Locator = Any


class SearchDropdownUtils:
    @staticmethod
    def __selectSearchDropdownValueByDropdownId(
        page: Page, component_id: str, value: str
    ):
        if not component_id:
            raise ValueError("Invalid component_id provided.")

        input_component_id = f"{component_id}_searchInput"
        input_component = ComponentUtils.findComponentById(page, input_component_id)
        InputUtils._setValueByComponent(page, input_component, value)

        dropdown_option_id = f"{component_id}_list"
        value_literal = ComponentUtils.xpath_literal(value)
        xpath = (
            f".//ul[@id={ComponentUtils.xpath_literal(dropdown_option_id)}]"
            f"/li[./div[normalize-space(translate(., '\u00a0', ' '))={value_literal}]][1]"
        )
        component = ComponentUtils.waitForComponentToBeVisibleByXpath(page, xpath)
        ComponentUtils.click(page, component)
        return component

    @staticmethod
    def __selectSearchDropdownValueByPartialLabelText(
        page: Page, label: str, value: str
    ):
        label_literal = ComponentUtils.xpath_literal(label)
        # Complex nested XPath breaks down as:
        # .//div[./div/span[contains(...)]] - Find parent div containing span with partial label match
        # /div/div/div/div[@role="combobox" - Navigate through nested divs to find the combobox
        # and not(@aria-disabled="true")] - Ensure combobox is enabled
        xpath = (
            ".//div[./div/span[contains(normalize-space(translate(., '\u00a0', ' ')), "
            f'{label_literal})]]/div/div/div/div[@role="combobox" and not(@aria-disabled="true")]'
        )
        combobox = ComponentUtils.waitForComponentToBeVisibleByXpath(page, xpath)
        return SearchDropdownUtils.__selectSearchDropdownValueByComboboxComponent(
            page, combobox, value
        )

    @staticmethod
    def __selectSearchDropdownValueByLabelText(page: Page, label: str, value: str):
        label_literal = ComponentUtils.xpath_literal(label)
        # Complex nested XPath breaks down as:
        # .//div[./div/span[...="label"]] - Find parent div with span matching exact label
        # /div/div/div/div[@role="combobox" - Navigate through nested divs to combobox
        # and not(@aria-disabled="true")] - Ensure combobox is enabled
        xpath = (
            ".//div[./div/span[normalize-space(translate(., '\u00a0', ' '))="
            f'{label_literal}]]/div/div/div/div[@role="combobox" and not(@aria-disabled="true")]'
        )
        combobox = ComponentUtils.waitForComponentToBeVisibleByXpath(page, xpath)
        return SearchDropdownUtils.__selectSearchDropdownValueByComboboxComponent(
            page, combobox, value
        )

    @staticmethod
    def __selectSearchDropdownValueByComboboxComponent(
        page: Page, combobox: Locator, value: str
    ):
        combobox_id = combobox.get_attribute("id")
        if not combobox_id:
            raise ValueError("Combobox element does not have an 'id' attribute.")

        if combobox_id.endswith("_value"):
            component_id = combobox_id.rsplit("_value", 1)[0]
        else:
            component_id = combobox_id

        ComponentUtils.click(page, combobox)
        SearchDropdownUtils.__selectSearchDropdownValueByDropdownId(
            page, component_id, value
        )
        return combobox

    @staticmethod
    def selectSearchDropdownValueByLabelText(
        page: Page, dropdown_label: str, value: str
    ):
        """Select a search dropdown value by exact label text.

        Args:
            page: Playwright Page object.
            dropdown_label: Exact text to match in the search dropdown label.
            value: The option value to select.

        Returns:
            Locator: The combobox element.

        Raises:
            TimeoutError: If dropdown or option is not found.
        """
        return SearchDropdownUtils.__selectSearchDropdownValueByLabelText(
            page, dropdown_label, value
        )
        return SearchDropdownUtils.__selectSearchDropdownValueByLabelText(
            page, dropdown_label, value
        )

    @staticmethod
    def selectSearchDropdownValueByPartialLabelText(
        page: Page, dropdown_label: str, value: str
    ):
        """Select a search dropdown value by partial label text match.

        Args:
            page: Playwright Page object.
            dropdown_label: Partial text to match in the search dropdown label.
            value: The option value to select.

        Returns:
            Locator: The combobox element.

        Raises:
            TimeoutError: If dropdown or option is not found.
        """
        return SearchDropdownUtils.__selectSearchDropdownValueByPartialLabelText(
            page, dropdown_label, value
        )
