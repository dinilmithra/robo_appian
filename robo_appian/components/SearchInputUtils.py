from typing import Any

from playwright.sync_api import expect

from robo_appian.utils.ComponentUtils import ComponentUtils

Page = Any
Locator = Any


class SearchInputUtils:
    """Convenience helper facade for Appian search input interactions."""

    @staticmethod
    def select(page: Page, label: str, value: str) -> None:

        locator = page.get_by_role("combobox", name=label)
        expect(locator).to_be_visible() 
        aria_controls_value = locator.get_attribute("aria-controls")

        locator.fill("")
        locator.fill(value)

        listbox_locator = page.locator(f'[id="{aria_controls_value}"]').first
        expect(listbox_locator).to_be_visible() 

        first_valid_option_locator = listbox_locator.get_by_role("option").filter(has_text=value).first
        expect(first_valid_option_locator).to_be_visible() 
        first_valid_option_locator.click()

        ComponentUtils.waitForAppianActionCompleted(page)

        

        
