from typing import Any

from robo_appian.utils.ComponentUtils import ComponentUtils

Page = Any
Locator = Any


class DropdownUtils:
    @staticmethod
    def __findComboboxByLabelText(page: Page, label: str, is_partial_text: bool = False):
        label_literal = ComponentUtils.xpath_literal(label.strip())
        span_text = ComponentUtils.xpath_text_with_normalized_nbsp(".")
        label_predicate = ComponentUtils.xpath_trim_equals(".", label)
        if is_partial_text:
            xpath = (
                f"//span[contains({span_text}, "
                f'{label_literal})]/ancestor::div[@role="presentation"][1]'
                f'//div[@role="combobox" and not(@aria-disabled="true")]'
            )
        else:
            xpath = (
                f"//span[{label_predicate}]/ancestor::div[@role=\"presentation\"][1]"
                f'//div[@role="combobox" and not(@aria-disabled="true")]'
            )
        return ComponentUtils.waitForComponentToBeVisibleByXpath(page, xpath)

    @staticmethod
    def __clickCombobox(page: Page, combobox: Locator):
        ComponentUtils.click(page, combobox)

    @staticmethod
    def __findDropdownOptionId(combobox: Locator):
        dropdown_option_id = combobox.get_attribute("aria-controls")
        if dropdown_option_id is None:
            raise ValueError('Dropdown combobox is missing "aria-controls" attribute.')
        return dropdown_option_id

    @staticmethod
    def __checkDropdownOptionValueExistsByDropdownOptionId(
        page: Page, dropdown_option_id: str, value: str
    ):
        value_predicate = ComponentUtils.xpath_trim_equals(".", value)
        xpath = (
            f".//div/ul[@id={ComponentUtils.xpath_literal(dropdown_option_id)}]"
            f"/li[./div[{value_predicate}]]"
        )
        return ComponentUtils.checkComponentExistsByXpath(page, xpath)

    @staticmethod
    def __selectDropdownValueByDropdownOptionId(
        page: Page, dropdown_option_id: str, value: str
    ):
        value_predicate = ComponentUtils.xpath_trim_equals(".", value)
        option_xpath = (
            f".//div/ul[@id={ComponentUtils.xpath_literal(dropdown_option_id)}]"
            f"/li[./div[{value_predicate}]]"
        )
        component = ComponentUtils.waitForComponentToBeVisibleByXpath(
            page, option_xpath
        )
        ComponentUtils.click(page, component)
        return component

    @staticmethod
    def __selectDropdownValueByPartialLabelText(page: Page, label: str, value: str):
        combobox = DropdownUtils.__findComboboxByLabelText(page, label, True)
        DropdownUtils.__clickCombobox(page, combobox)
        dropdown_option_id = DropdownUtils.__findDropdownOptionId(combobox)
        DropdownUtils.__selectDropdownValueByDropdownOptionId(
            page, dropdown_option_id, value
        )
        return combobox

    @staticmethod
    def __selectDropdownValueByLabelText(page: Page, label: str, value: str):
        combobox = DropdownUtils.__findComboboxByLabelText(page, label)
        DropdownUtils.__clickCombobox(page, combobox)
        dropdown_option_id = DropdownUtils.__findDropdownOptionId(combobox)
        DropdownUtils.__selectDropdownValueByDropdownOptionId(
            page, dropdown_option_id, value
        )
        return combobox

    @staticmethod
    def checkReadOnlyStatusByLabelText(page: Page, label: str):
        """Check if a dropdown is read-only by label text.

        Args:
            page: Playwright Page object.
            label: Exact text to match in the dropdown label.

        Returns:
            bool: True if dropdown is read-only, False otherwise.
        """
        label_predicate = ComponentUtils.xpath_trim_equals(".", label)
        xpath = (
            f"//span[{label_predicate}]/ancestor::div[@role=\"presentation\"][1]"
            '//div[@aria-labelledby and not(@role="combobox")]'
        )
        return ComponentUtils.checkComponentExistsByXpath(page, xpath)

    @staticmethod
    def checkEditableStatusByLabelText(page: Page, label: str):
        """Check if a dropdown is editable (not read-only) by label text.

        Args:
            page: Playwright Page object.
            label: Exact text to match in the dropdown label.

        Returns:
            bool: True if dropdown is editable, False otherwise.
        """
        label_predicate = ComponentUtils.xpath_trim_equals(".", label)
        xpath = (
            f"//span[{label_predicate}]/ancestor::div[@role=\"presentation\"][1]"
            '//div[@role="combobox" and not(@aria-disabled="true")]'
        )
        return ComponentUtils.checkComponentExistsByXpath(page, xpath)

    @staticmethod
    def waitForDropdownToBeEnabled(
        page: Page, label: str, wait_interval: float = 0.5, timeout: int = 2
    ):
        """Wait for a dropdown to become enabled/editable.

        Args:
            page: Playwright Page object.
            label: Exact text to match in the dropdown label.
            wait_interval: Time to wait between retries in seconds. Default: 0.5.
            timeout: Maximum time to wait in seconds. Default: 2.

        Returns:
            bool: True if dropdown becomes enabled within timeout, False otherwise.
        """
        return bool(
            ComponentUtils.retry_until(
                lambda: DropdownUtils.checkEditableStatusByLabelText(page, label),
                timeout=timeout,
                wait_interval=wait_interval,
                timeout_result=False,
            )
        )

    @staticmethod
    def selectDropdownValueByComboboxComponent(
        page: Page, combobox: Locator, value: str
    ):
        """Select a dropdown value using a combobox component locator.

        Args:
            page: Playwright Page object.
            combobox: Locator pointing to a combobox element.
            value: The option value to select.

        Returns:
            Locator: The combobox element.

        Raises:
            ValueError: If combobox is missing 'aria-controls' attribute.
            TimeoutError: If option is not found.
        """
        dropdown_option_id = DropdownUtils.__findDropdownOptionId(combobox)
        DropdownUtils.__clickCombobox(page, combobox)
        DropdownUtils.__selectDropdownValueByDropdownOptionId(
            page, dropdown_option_id, value
        )
        return combobox

    @staticmethod
    def selectDropdownValueByLabelText(page: Page, dropdown_label: str, value: str):
        """Select a dropdown value by exact label text.

        Args:
            page: Playwright Page object.
            dropdown_label: Exact text to match in the dropdown label.
            value: The option value to select.

        Returns:
            Locator: The combobox element.

        Raises:
            TimeoutError: If dropdown or option is not found.
        """
        return DropdownUtils.__selectDropdownValueByLabelText(
            page, dropdown_label, value
        )

    @staticmethod
    def selectDropdownValueByPartialLabelText(
        page: Page, dropdown_label: str, value: str
    ):
        """Select a dropdown value by partial label text match.

        Args:
            page: Playwright Page object.
            dropdown_label: Partial text to match in the dropdown label.
            value: The option value to select.

        Returns:
            Locator: The combobox element.

        Raises:
            TimeoutError: If dropdown or option is not found.
        """
        return DropdownUtils.__selectDropdownValueByPartialLabelText(
            page, dropdown_label, value
        )

    @staticmethod
    def checkDropdownOptionValueExists(page: Page, dropdown_label: str, value: str):
        """Check if a dropdown option value exists.

        Args:
            page: Playwright Page object.
            dropdown_label: Exact text to match in the dropdown label.
            value: The option value to check for.

        Returns:
            bool: True if the option exists, False otherwise.
        """
        combobox = DropdownUtils.__findComboboxByLabelText(page, dropdown_label)
        DropdownUtils.__clickCombobox(page, combobox)
        dropdown_option_id = DropdownUtils.__findDropdownOptionId(combobox)
        return DropdownUtils.__checkDropdownOptionValueExistsByDropdownOptionId(
            page, dropdown_option_id, value
        )

    @staticmethod
    def getDropdownOptionValues(page: Page, dropdown_label: str) -> list[str]:
        combobox = DropdownUtils.__findComboboxByLabelText(page, dropdown_label)
        opened_here = combobox.get_attribute("aria-expanded") != "true"
        if opened_here:
            DropdownUtils.__clickCombobox(page, combobox)
        dropdown_option_id = DropdownUtils.__findDropdownOptionId(combobox)

        xpath = f'//ul[@id={ComponentUtils.xpath_literal(dropdown_option_id)}]//li[@role="option"]/div'
        option_elements = page.locator(f"xpath={xpath}")

        option_texts: list[str] = []
        for idx in range(option_elements.count()):
            text = option_elements.nth(idx).inner_text().strip()
            if text:
                option_texts.append(text)

        if opened_here and combobox.get_attribute("aria-expanded") == "true":
            DropdownUtils.__clickCombobox(page, combobox)
        return option_texts

    @staticmethod
    def waitForDropdownValuesToBeChanged(
        page: Page,
        dropdown_label: str,
        initial_values: list[str],
        poll_frequency: float = 0.5,
        timeout: int = 2,
    ):
        return bool(
            ComponentUtils.retry_until(
                lambda: DropdownUtils.getDropdownOptionValues(page, dropdown_label)
                != initial_values,
                timeout=timeout,
                wait_interval=poll_frequency,
                timeout_result=False,
            )
        )
