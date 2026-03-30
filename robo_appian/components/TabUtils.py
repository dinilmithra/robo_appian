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
        label_predicate = ComponentUtils.xpath_trim_equals(".", label)
        xpath = (
            f"//div[@role=\"link\"][.//p[{label_predicate}]]"
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
        selected_tab_predicate = ComponentUtils.xpath_trim_equals(".", "Selected Tab.")
        selected_indicator = component.locator(
            f"xpath=.//span[{selected_tab_predicate}]"
        )
        return selected_attr == "true" or selected_indicator.count() > 0
