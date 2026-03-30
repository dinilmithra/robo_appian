from playwright.sync_api import Page

from robo_appian.utils.ComponentUtils import ComponentUtils


class LinkUtils:
    @staticmethod
    def find(page: Page, label: str):
        """Find a link by exact label text.

        Args:
            page: Playwright Page object.
            label: Exact text to match in the link.

        Returns:
            Locator: The link element.

        Raises:
            TimeoutError: If link is not found or not visible.
        """
        label_literal = ComponentUtils.xpath_literal(label)
        xpath = (
            ".//a[normalize-space(translate(., '\u00a0', ' '))="
            f'{label_literal} and not(ancestor::*[@aria-hidden="true"])'
            ' and not(ancestor-or-self::*[contains(@class, "---hidden")])]'
        )
        return ComponentUtils.waitForComponentToBeVisibleByXpath(page, xpath)

    @staticmethod
    def click(page: Page, label: str):
        """Click a link by label text.

        Args:
            page: Playwright Page object.
            label: Exact text to match in the link.

        Returns:
            Locator: The link element that was clicked.

        Raises:
            TimeoutError: If link is not found or not visible.
        """
        component = LinkUtils.find(page, label)
        ComponentUtils.click(page, component)
        return component
