from typing import Any

from robo_appian.components.InputUtils import InputUtils
from robo_appian.utils.ComponentUtils import ComponentUtils

Page = Any


class DateUtils:
    @staticmethod
    def __findComponent(page: Page, label: str):
        label_predicate = ComponentUtils.xpath_trim_equals(".", label)
        visible_predicate = ComponentUtils.xpath_visible_predicate()
        xpath = (
            f".//div[./div/label[{label_predicate}]]/div/div/div/input[{visible_predicate}]"
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
