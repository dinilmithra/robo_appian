from typing import Any

from robo_appian.components.InputUtils import InputUtils
from robo_appian.utils.ComponentUtils import ComponentUtils

Page = Any


class DateUtils:
    @staticmethod
    def __findComponent(page: Page, label: str):
        label_literal = ComponentUtils.xpath_literal(label)
        xpath = (
            ".//div[./div/label[normalize-space(translate(., '\u00a0', ' '))="
            f"{label_literal}]]/div/div/div/input"
        )
        return ComponentUtils.waitForComponentToBeVisibleByXpath(page, xpath)

    @staticmethod
    def setValueByLabelText(page: Page, label: str, value: str):
        """Set a date input value by label text.

        Args:
            page: Playwright Page object.
            label: Exact text to match in the date input label.
            value: The date value (format: MM/DD/YYYY).

        Returns:
            Locator: The date input element that was filled.

        Raises:
            TimeoutError: If date input is not found or not visible.
        """
        component = DateUtils.__findComponent(page, label)
        InputUtils._setValueByComponent(page, component, value)
        component.blur()
        return component

    @staticmethod
    def clickByLabelText(page: Page, label: str):
        """Click a date input by label text.

        Args:
            page: Playwright Page object.
            label: Exact text to match in the date input label.

        Returns:
            Locator: The date input element that was clicked.

        Raises:
            TimeoutError: If date input is not found or not visible.
        """
        component = DateUtils.__findComponent(page, label)
        ComponentUtils.click(page, component)
        return component
