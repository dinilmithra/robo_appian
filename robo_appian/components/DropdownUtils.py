from typing import Any

from robo_appian.utils.ComponentUtils import ComponentUtils

Page = Any
Locator = Any


class DropdownUtils:
    @staticmethod
    def __findComboboxByLabelText(page: Page, label: str, isPartialText: bool = False):
        label_literal = ComponentUtils.xpath_literal(label)
        if isPartialText:
            xpath = (
                "//span[contains(normalize-space(translate(., '\u00a0', ' ')), "
                f'{label_literal})]/ancestor::div[@role="presentation"][1]'
                f'//div[@role="combobox" and not(@aria-disabled="true")]'
            )
        else:
            xpath = (
                "//span[normalize-space(translate(., '\u00a0', ' '))="
                f'{label_literal}]/ancestor::div[@role="presentation"][1]'
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
        value_literal = ComponentUtils.xpath_literal(value)
        xpath = (
            f".//div/ul[@id={ComponentUtils.xpath_literal(dropdown_option_id)}]"
            f"/li[./div[normalize-space(translate(., '\u00a0', ' '))={value_literal}]]"
        )
        return ComponentUtils.checkComponentExistsByXpath(page, xpath)

    @staticmethod
    def __selectDropdownValueByDropdownOptionId(
        page: Page, dropdown_option_id: str, value: str
    ):
        value_literal = ComponentUtils.xpath_literal(value)
        option_xpath = (
            f".//div/ul[@id={ComponentUtils.xpath_literal(dropdown_option_id)}]"
            f"/li[./div[normalize-space(translate(., '\u00a0', ' '))={value_literal}]]"
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
        label_literal = ComponentUtils.xpath_literal(label)
        xpath = (
            "//span[normalize-space(translate(., '\u00a0', ' '))="
            f'{label_literal}]/ancestor::div[@role="presentation"][1]'
            '//div[@aria-labelledby and not(@role="combobox")]'
        )
        return ComponentUtils.checkComponentExistsByXpath(page, xpath)

    @staticmethod
    def checkEditableStatusByLabelText(page: Page, label: str):
        label_literal = ComponentUtils.xpath_literal(label)
        xpath = (
            "//span[normalize-space(translate(., '\u00a0', ' '))="
            f'{label_literal}]/ancestor::div[@role="presentation"][1]'
            '//div[@role="combobox" and not(@aria-disabled="true")]'
        )
        return ComponentUtils.checkComponentExistsByXpath(page, xpath)

    @staticmethod
    def waitForDropdownToBeEnabled(
        page: Page, label: str, wait_interval: float = 0.5, timeout: int = 2
    ):
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
        dropdown_option_id = DropdownUtils.__findDropdownOptionId(combobox)
        DropdownUtils.__clickCombobox(page, combobox)
        DropdownUtils.__selectDropdownValueByDropdownOptionId(
            page, dropdown_option_id, value
        )
        return combobox

    @staticmethod
    def selectDropdownValueByLabelText(page: Page, dropdown_label: str, value: str):
        return DropdownUtils.__selectDropdownValueByLabelText(
            page, dropdown_label, value
        )

    @staticmethod
    def selectDropdownValueByPartialLabelText(
        page: Page, dropdown_label: str, value: str
    ):
        return DropdownUtils.__selectDropdownValueByPartialLabelText(
            page, dropdown_label, value
        )

    @staticmethod
    def checkDropdownOptionValueExists(page: Page, dropdown_label: str, value: str):
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
