from typing import Any

from robo_appian.utils.ComponentUtils import ComponentUtils

Page = Any
Locator = Any


class InputUtils:
    @staticmethod
    def __findComponentByPartialLabel(page: Page, label: str):
        label_literal = ComponentUtils.xpath_literal(label)
        xpath = (
            ".//div/label[contains(translate(., '\u00a0', ' '), "
            f"{label_literal})]"
        )
        label_component = ComponentUtils.waitForComponentToBeVisibleByXpath(page, xpath)

        input_id = label_component.get_attribute("for")
        if input_id is None:
            raise ValueError(
                f"Label element with text '{label}' is missing the 'for' attribute that links it to an input field."
            )

        component = ComponentUtils.findComponentById(page, input_id)
        return component

    @staticmethod
    def __findComponentByLabel(page: Page, label: str):
        label_literal = ComponentUtils.xpath_literal(label)
        xpath = (
            ".//div/label[translate(., '\u00a0', ' ')="
            f"{label_literal}]"
        )
        label_component = ComponentUtils.waitForComponentToBeVisibleByXpath(page, xpath)
        input_id = label_component.get_attribute("for")
        if input_id is None:
            raise ValueError(
                f"Label component with text '{label}' does not have a 'for' attribute."
            )

        component = ComponentUtils.findComponentById(page, input_id)
        return component

    @staticmethod
    def _setValueByComponent(page: Page, component: Locator, value: str):
        input_value = "" if value is None else str(value)
        component.wait_for(state="visible")
        component.scroll_into_view_if_needed()
        component.click()
        component.fill("")
        component.fill(input_value)
        return component

    @staticmethod
    def setValueByPartialLabelText(page: Page, label: str, value: str):
        component = InputUtils.__findComponentByPartialLabel(page, label)
        return InputUtils._setValueByComponent(page, component, value)

    @staticmethod
    def setValueByLabelText(page: Page, label: str, value: str):
        component = InputUtils.__findComponentByLabel(page, label)
        return InputUtils._setValueByComponent(page, component, value)

    @staticmethod
    def setValueById(page: Page, id: str, value: str):
        component = ComponentUtils.findComponentById(page, id)
        return InputUtils._setValueByComponent(page, component, value)

    @staticmethod
    def setValueByPlaceholderText(page: Page, text: str, value: str):
        xpath = f".//input[@placeholder={ComponentUtils.xpath_literal(text)}]"
        component = ComponentUtils.waitForComponentToBeVisibleByXpath(page, xpath)
        return InputUtils._setValueByComponent(page, component, value)
