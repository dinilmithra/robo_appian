from playwright.sync_api import Page, expect


class AppianUtils:
    """High-level convenience utilities for common Appian page actions."""

    @staticmethod
    def waitForVisibleElementByText(page: Page, text: str):
        """Wait for an element to become visible by exact text match."""

        # 1. get_by_text(exact=True) auto-targets the deepest element, handling NBSP & whitespace.
        # 2. filter(visible=True) ignores elements hidden by Appian's CSS (like '---hidden').
        # 3. .first prevents strict mode violations if the text appears multiple times.
        locator = page.get_by_text(text, exact=True).filter(visible=True).first

        # 4. expect() automatically polls and waits for the element to appear
        expect(locator).to_be_visible()

        return locator
