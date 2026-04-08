import re
from typing import Any

from robo_appian.utils.ComponentUtils import ComponentUtils

Page = Any
Locator = Any


class ButtonUtils:
    """Playwright helper for clicking Appian buttons when they become enabled."""

    @staticmethod
    def __exactTextPattern(text: str) -> re.Pattern[str]:
        return re.compile(rf"^\s*{re.escape(text)}\s*$", re.IGNORECASE)

    @staticmethod
    def __partialTextPattern(text: str) -> re.Pattern[str]:
        return re.compile(re.escape(text.strip()), re.IGNORECASE)

    @staticmethod
    def __findButton(page: Page, label: str) -> Locator:
        exact_match = page.get_by_role(
            "button",
            name=ButtonUtils.__exactTextPattern(label),
        ).first
        if exact_match.count() > 0:
            return exact_match

        return page.get_by_role(
            "button",
            name=ButtonUtils.__partialTextPattern(label),
        ).first

    @staticmethod
    def __clickWhenVisible(page: Page, component: Locator) -> None:
        component.wait_for(state="visible")
        component.scroll_into_view_if_needed()
        component.click()
        ComponentUtils.waitForAppianActionCompleted(page)

    @staticmethod
    def click(
        page: Page,
        label: str = "Submit",
    ) -> None:
        """Wait for the requested button to become visible, click it, and wait for Appian to finish processing."""
        button = ButtonUtils.__findButton(page, label)
        ButtonUtils.__clickWhenVisible(page, button)

    @staticmethod
    def clickById(
        page: Page,
        id: str,
    ) -> None:
        """Wait for a visible element with the given id, then click it using Playwright's default waiting."""
        button = page.locator(f'[id="{id}"]').first
        ButtonUtils.__clickWhenVisible(page, button)
