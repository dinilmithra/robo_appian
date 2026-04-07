import re
import time
from typing import Any

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

Page = Any
Locator = Any


class DropdownUtils:
    """Playwright helper for selecting Appian dropdown values only when editable."""

    @staticmethod
    def __exactTextPattern(text: str) -> re.Pattern[str]:
        return re.compile(rf"^\s*{re.escape(text)}\s*$", re.IGNORECASE)

    @staticmethod
    def __partialTextPattern(text: str) -> re.Pattern[str]:
        return re.compile(re.escape(text.strip()), re.IGNORECASE)

    @staticmethod
    def __ensureComponentVisible(
        component: Locator,
        label: str,
        component_type: str,
    ) -> Locator:
        try:
            component.wait_for(state="visible")
            return component
        except PlaywrightTimeoutError as exc:
            raise AssertionError(
                f"Expected visible {component_type} for '{label}', but it was not visible."
            ) from exc

    @staticmethod
    def __findLabelElement(page: Page, label: str) -> Locator:
        exact_match = page.locator("label, span").filter(
            has_text=DropdownUtils.__exactTextPattern(label)
        ).first
        if exact_match.count() > 0:
            return DropdownUtils.__ensureComponentVisible(exact_match, label, "label")

        partial_match = page.locator("label, span").filter(
            has_text=DropdownUtils.__partialTextPattern(label)
        ).first
        return DropdownUtils.__ensureComponentVisible(partial_match, label, "label")

    @staticmethod
    def __findControlByLabel(page: Page, label: str) -> Locator | None:
        label_element = DropdownUtils.__findLabelElement(page, label)
        if label_element.count() == 0:
            return None

        control_id = label_element.get_attribute("for")
        if not control_id:
            return None

        control = page.locator(f'[id="{control_id}"]').first
        if control.count() == 0:
            return None

        return control

    @staticmethod
    def __findLabeledContainer(page: Page, label: str) -> Locator:
        label_element = DropdownUtils.__findLabelElement(page, label)
        if label_element.count() > 0:
            container = label_element.locator(
                "xpath=ancestor::div[@role='presentation'][1]"
            ).first
            if container.count() > 0:
                return container

        label_pattern = DropdownUtils.__exactTextPattern(label)
        return page.locator("div[role='presentation']").filter(
            has=page.locator("label, span").filter(has_text=label_pattern)
        ).first

    @staticmethod
    def __findCombobox(page: Page, label: str) -> Locator:
        exact_role_match = page.get_by_role(
            "combobox",
            name=DropdownUtils.__exactTextPattern(label),
        ).first
        if exact_role_match.count() > 0:
            return exact_role_match

        partial_role_match = page.get_by_role(
            "combobox",
            name=DropdownUtils.__partialTextPattern(label),
        ).first
        if partial_role_match.count() > 0:
            return partial_role_match

        control = DropdownUtils.__findControlByLabel(page, label)
        if control is not None:
            if control.get_attribute("role") == "combobox":
                return control

            parent_combobox = control.locator(
                "xpath=ancestor-or-self::*[@role='combobox'][1]"
            ).first
            if parent_combobox.count() > 0:
                return parent_combobox

        return DropdownUtils.__findLabeledContainer(page, label).locator(
            'div[role="combobox"], input[role="combobox"]'
        ).first

    @staticmethod
    def __isDropdownEditable(combobox: Locator) -> bool:
        try:
            return (
                combobox.count() > 0
                and combobox.is_visible()
                and combobox.get_attribute("aria-disabled") != "true"
                and not combobox.is_disabled()
            )
        except Exception:
            return False

    @staticmethod
    def __waitUntilDropdownEditable(
        page: Page,
        label: str,
        timeout_seconds: int = 20,
        poll_interval_seconds: int = 1,
    ) -> Locator:
        poll_interval_ms = int(poll_interval_seconds * 1000)
        combobox = DropdownUtils.__ensureComponentVisible(
            DropdownUtils.__findCombobox(page, label),
            label,
            "dropdown",
        )
        deadline = time.monotonic() + timeout_seconds

        while time.monotonic() < deadline:
            if DropdownUtils.__isDropdownEditable(combobox):
                return combobox
            page.wait_for_timeout(poll_interval_ms)

        return combobox

    @staticmethod
    def __getDropdownOptionLocators(
        page: Page,
        combobox: Locator,
        value: str,
        poll_interval_seconds: int,
    ) -> list[Locator]:
        dropdown_option_id = None
        controls_deadline = time.monotonic() + max(poll_interval_seconds, 1)
        while time.monotonic() < controls_deadline:
            dropdown_option_id = combobox.get_attribute("aria-controls")
            if dropdown_option_id:
                break
            page.wait_for_timeout(100)

        option_locators: list[Locator] = []
        if dropdown_option_id:
            scoped_options = page.locator(
                f'ul[id="{dropdown_option_id}"] li, [id="{dropdown_option_id}"] [role="option"]'
            )
            option_locators.append(
                scoped_options.filter(has_text=DropdownUtils.__exactTextPattern(value)).first
            )
            option_locators.append(
                scoped_options.filter(has_text=DropdownUtils.__partialTextPattern(value)).first
            )

        option_locators.append(
            page.get_by_role("option", name=DropdownUtils.__exactTextPattern(value)).first
        )
        option_locators.append(
            page.get_by_role("option", name=DropdownUtils.__partialTextPattern(value)).first
        )
        option_locators.append(
            page.locator('[role="option"], li').filter(
                has_text=DropdownUtils.__partialTextPattern(value)
            ).first
        )
        return option_locators

    @staticmethod
    def __selectDropdownValueByCombobox(
        page: Page,
        combobox: Locator,
        value: str,
        option_timeout_seconds: int,
        poll_interval_seconds: int,
        dropdown_name: str,
    ) -> bool:
        combobox.scroll_into_view_if_needed()
        combobox.click()

        option_locators = DropdownUtils.__getDropdownOptionLocators(
            page,
            combobox,
            value,
            poll_interval_seconds,
        )

        deadline = time.monotonic() + option_timeout_seconds
        while time.monotonic() < deadline:
            for option in option_locators:
                try:
                    if option.count() == 0 or not option.is_visible():
                        continue
                    option.scroll_into_view_if_needed()
                    option.click()
                    page.wait_for_timeout(250)
                    return True
                except Exception:
                    continue
            page.wait_for_timeout(200)

        print(
            f"Skipping '{dropdown_name}' because option '{value}' was not available in time."
        )
        return False

    @staticmethod
    def selectDropdownIfEditable(
        page: Page,
        label: str,
        value: str,
        editable_timeout_seconds: int = 5,
        poll_interval_seconds: int = 1,
    ) -> bool:
        """Select a dropdown value after waiting for the labeled combobox to become editable."""
        combobox = DropdownUtils.__waitUntilDropdownEditable(
            page,
            label,
            timeout_seconds=editable_timeout_seconds,
            poll_interval_seconds=poll_interval_seconds,
        )
        if not DropdownUtils.__isDropdownEditable(combobox):
            print(
                f"Skipping '{label}' because the dropdown is not editable within "
                f"{editable_timeout_seconds} seconds."
            )
            return False

        return DropdownUtils.__selectDropdownValueByCombobox(
            page,
            combobox,
            value,
            option_timeout_seconds=editable_timeout_seconds,
            poll_interval_seconds=poll_interval_seconds,
            dropdown_name=label,
        )

    @staticmethod
    def selectDropdownValueByComboboxComponent(
        page: Page,
        combobox: Locator,
        value: str,
        option_timeout_seconds: int = 5,
        poll_interval_seconds: int = 1,
    ) -> bool:
        """Select a dropdown value using an existing combobox locator."""
        combobox = DropdownUtils.__ensureComponentVisible(
            combobox,
            "provided combobox",
            "dropdown",
        )
        return DropdownUtils.__selectDropdownValueByCombobox(
            page,
            combobox,
            value,
            option_timeout_seconds=option_timeout_seconds,
            poll_interval_seconds=poll_interval_seconds,
            dropdown_name="provided combobox",
        )

    @staticmethod
    def checkDropdownOptionValueExists(
        page: Page,
        label: str,
        value: str,
        option_timeout_seconds: int = 5,
        poll_interval_seconds: int = 1,
    ) -> bool:
        """Check whether a dropdown option exists for the labeled combobox."""
        combobox = DropdownUtils.__ensureComponentVisible(
            DropdownUtils.__findCombobox(page, label),
            label,
            "dropdown",
        )
        combobox.scroll_into_view_if_needed()
        combobox.click()

        option_locators = DropdownUtils.__getDropdownOptionLocators(
            page,
            combobox,
            value,
            poll_interval_seconds,
        )

        deadline = time.monotonic() + option_timeout_seconds
        while time.monotonic() < deadline:
            for option in option_locators:
                try:
                    if option.count() > 0 and option.is_visible():
                        return True
                except Exception:
                    continue
            page.wait_for_timeout(200)

        return False
