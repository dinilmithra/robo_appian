from playwright.sync_api import Page

from robo_appian.utils.ComponentUtils import ComponentUtils


class TabUtils:
    @staticmethod
    def findTabByLabelText(page: Page, label: str):
        """Find a tab element by exact label text.

        Args:
            page: Playwright Page object.
            label: Exact text to match in the tab label.

        Returns:
            Locator: The tab element.

        Raises:
            TimeoutError: If tab is not found or not visible.
        """
        label_literal = ComponentUtils.xpath_literal(label)
        xpath = (
            "//div[@role=\"link\"][.//p[normalize-space(translate(., '\u00a0', ' '))="
            f"{label_literal}]]"
        )
        return ComponentUtils.waitForComponentToBeVisibleByXpath(page, xpath)

    @staticmethod
    def selectTabByLabelText(page: Page, label: str):
        """Click and select a tab by label text.

        Args:
            page: Playwright Page object.
            label: Exact text to match in the tab label.

        Raises:
            TimeoutError: If tab is not found or not visible.
        """
        component = TabUtils.findTabByLabelText(page, label)
        ComponentUtils.click(page, component)

    @staticmethod
    def checkTabSelectedByLabelText(page: Page, label: str):
        """Check if a tab is currently selected.

        Args:
            page: Playwright Page object.
            label: Exact text to match in the tab label.

        Returns:
            bool: True if the tab is selected, False otherwise.
        """
        component = TabUtils.findTabByLabelText(page, label)
        selected_attr = component.get_attribute("aria-selected")
        selected_indicator = component.locator(
            'xpath=.//span[normalize-space(.)="Selected Tab."]'
        )
        return selected_attr == "true" or selected_indicator.count() > 0
