from playwright.sync_api import Locator, Page


class InputUtils:
    """Helper utilities for interacting with text inputs."""

    @staticmethod
    def fill_value_by_locator(locator: Locator, value: str) -> Locator: 
        locator.wait_for(state="visible")
        locator.fill("" if value is None else str(value))
        locator.blur()
        return locator

    @staticmethod
    def fill_value_by_id(page: Page, component_id: str, value: str) -> Locator:
        """Fill a text input using its component ID."""
        locator = page.locator(f"#{component_id}").first
        return InputUtils.fill_value_by_locator(locator, value)

    @staticmethod
    def fill_value_by_placeholder(
        page: Page,
        placeholder_text: str,
        value: str,
    ) -> Locator:
        """Fill a text input using its placeholder text."""
        locator = page.get_by_placeholder(placeholder_text).first
        return InputUtils.fill_value_by_locator(locator, value)

    @staticmethod
    def fill_value(
        page: Page,
        label: str,
        value: str,
        exact_match: bool = True,
    ) -> Locator:
        """Fill a labeled text input and return the resolved locator."""
        locator = page.get_by_label(label, exact=exact_match).first
        return InputUtils.fill_value_by_locator(locator, value)
