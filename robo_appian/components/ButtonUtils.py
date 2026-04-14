import logging
import re

from playwright.sync_api import Locator, Page, expect

from robo_appian.utils.ComponentUtils import ComponentUtils

logger = logging.getLogger(__name__)


class ButtonUtils:
    """Playwright helper for clicking Appian buttons when they become enabled."""

    @staticmethod
    def __exact_text_pattern(text: str) -> re.Pattern[str]:
        return re.compile(rf"^\s*{re.escape(text)}\s*$", re.IGNORECASE)

    @staticmethod
    def __partial_text_pattern(text: str) -> re.Pattern[str]:
        return re.compile(re.escape(text.strip()), re.IGNORECASE)

    @staticmethod
    def __find_by_text(page: Page, label: str) -> Locator:
        """Find a visible button by accessible name using exact-match first, then partial-match fallback."""
        exact_match = page.get_by_role(
            "button",
            name=ButtonUtils.__exact_text_pattern(label),
        ).first
        if exact_match.count() > 0:
            return exact_match

        return page.get_by_role(
            "button",
            name=ButtonUtils.__partial_text_pattern(label),
        ).first

    @staticmethod
    def __find_by_id(page: Page, id: str) -> Locator:
        """Find a button by id."""
        return page.locator(f'[id="{id}"]').first

    @staticmethod
    def __click(page: Page, locator: Locator, description: str = "button") -> None:
        logger.info("Preparing to click %s", description)
        ComponentUtils.waitForAppianActionCompleted(page)
        expect(locator).to_be_visible()
        expect(locator).to_be_enabled()
        locator.scroll_into_view_if_needed()
        ComponentUtils.click(page, locator)
        ComponentUtils.waitForAppianActionCompleted(page)
        logger.info("Finished clicking %s", description)

    @staticmethod
    def clickById(
        page: Page,
        id: str,
    ) -> None:
        """Wait for a visible element with the given id, then click it."""
        locator = ButtonUtils.__find_by_id(page, id)
        ButtonUtils.__click(page, locator, f"button with id '{id}'")

    @staticmethod
    def click(
        page: Page,
        label: str = "Submit",
    ) -> None:
        """Wait for the requested button to become visible, click it, and wait for Appian to finish processing."""
        locator = ButtonUtils.__find_by_text(page, label)
        ButtonUtils.__click(page, locator, f"button '{label}'")
