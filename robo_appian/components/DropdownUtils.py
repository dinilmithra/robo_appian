import re
import time
from typing import Any, Optional

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
    def __getOuterHtml(component: Locator) -> str:
        try:
            if component.count() > 0:
                return str(component.first.evaluate("(node) => node.outerHTML"))
        except Exception:
            return ""
        return ""

    @staticmethod
    def __describeDropdownState(page: Page, label: str) -> tuple[str, Optional[Locator], str]:
        container = DropdownUtils.__findLabeledContainer(page, label).first
        container = DropdownUtils.__ensureComponentVisible(
            container, label, "dropdown container"
        )
        container_html = DropdownUtils.__getOuterHtml(container)

        editable_combobox = container.locator(
            '.DropdownWidget---dropdown_value[role="combobox"]:not(.DropdownWidget---is_disabled):not([aria-disabled="true"]), '
            'div[role="combobox"]:not([aria-disabled="true"]), '
            'input[role="combobox"]:not([disabled]):not([readonly])'
        ).first
        try:
            if editable_combobox.count() > 0 and editable_combobox.is_visible():
                return "editable", editable_combobox, container_html
        except Exception:
            pass

        readonly_display = container.locator(
            '.DropdownWidget---read_only, '
            '.DropdownWidget---readonly_value, '
            '[aria-readonly="true"], '
            '[data-readonly="true"], '
            '[aria-labelledby]:not([role="combobox"])'
        ).first
        try:
            if readonly_display.count() > 0 and readonly_display.is_visible():
                return "read-only", None, container_html
        except Exception:
            pass

        non_editable_combobox = container.locator(
            '.DropdownWidget---dropdown_value.DropdownWidget---is_disabled[role="combobox"], '
            'div[role="combobox"][aria-disabled="true"], '
            'input[role="combobox"][disabled], '
            'input[role="combobox"][readonly]'
        ).first
        try:
            if (
                non_editable_combobox.count() > 0
                and non_editable_combobox.is_visible()
            ):
                return "non-editable", non_editable_combobox, container_html
        except Exception:
            pass

        return "unknown", None, container_html

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
    def __findControlByLabel(page: Page, label: str) -> Optional[Locator]:
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
    def __waitForDropdownState(
        page: Page,
        label: str,
        timeout_seconds: int = 20,
        poll_interval_seconds: int = 1,
    ) -> tuple[str, Optional[Locator], str]:
        poll_interval_ms = int(poll_interval_seconds * 1000)
        deadline = time.monotonic() + timeout_seconds
        last_state = "unknown"
        last_combobox: Optional[Locator] = None
        last_html = ""

        while time.monotonic() < deadline:
            state, combobox, container_html = DropdownUtils.__describeDropdownState(
                page, label
            )
            last_state = state
            if combobox is not None:
                last_combobox = combobox
            if container_html:
                last_html = container_html

            if state == "editable" and combobox is not None:
                return state, combobox, last_html

            # Read-only fields use a distinct, stable HTML structure and should be skipped.
            if state == "read-only":
                return state, None, last_html

            page.wait_for_timeout(poll_interval_ms)

        return last_state, last_combobox, last_html

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
    def __waitForVisibleComponent(
        page: Page,
        components: list[Locator],
        timeout_seconds: int,
        poll_interval_seconds: int = 1,
    ) -> Optional[Locator]:
        poll_interval_ms = max(poll_interval_seconds * 1000, 100)
        deadline = time.monotonic() + timeout_seconds

        while time.monotonic() < deadline:
            for component in components:
                try:
                    if component.count() > 0 and component.is_visible():
                        return component
                except Exception:
                    continue
            page.wait_for_timeout(poll_interval_ms)

        return None

    @staticmethod
    def __selectDropdownValueByCombobox(
        page: Page,
        combobox: Locator,
        value: str,
        option_timeout_seconds: int,
        poll_interval_seconds: int,
        dropdown_name: str,
    ) -> bool:
        combobox = DropdownUtils.__ensureComponentVisible(
            combobox,
            dropdown_name,
            "dropdown",
        )
        combobox.scroll_into_view_if_needed()

        deadline = time.monotonic() + option_timeout_seconds
        while time.monotonic() < deadline:
            try:
                combobox.click()
            except Exception:
                page.wait_for_timeout(200)
                continue

            option_locators = DropdownUtils.__getDropdownOptionLocators(
                page,
                combobox,
                value,
                poll_interval_seconds,
            )
            remaining_seconds = max(int(deadline - time.monotonic()), 1)
            option = DropdownUtils.__waitForVisibleComponent(
                page,
                option_locators,
                timeout_seconds=min(max(poll_interval_seconds, 1), remaining_seconds),
                poll_interval_seconds=poll_interval_seconds,
            )
            if option is None:
                continue

            try:
                option.scroll_into_view_if_needed()
                option.click()
                page.wait_for_timeout(250)
                return True
            except Exception:
                page.wait_for_timeout(200)
                continue

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
        normalized_value = "" if value is None else str(value).strip()
        if not normalized_value:
            _, _, container_html = DropdownUtils.__describeDropdownState(page, label)
            print(
                f"Skipping '{label}' because no dropdown value was provided. "
                f"Container HTML: {container_html}"
            )
            return False

        state, combobox, container_html = DropdownUtils.__waitForDropdownState(
            page,
            label,
            timeout_seconds=editable_timeout_seconds,
            poll_interval_seconds=poll_interval_seconds,
        )
        if state == "read-only":
            print(
                f"Skipping '{label}' because the dropdown is read-only. "
                f"Container HTML: {container_html}"
            )
            return False

        if combobox is None or not DropdownUtils.__isDropdownEditable(combobox):
            print(
                f"Skipping '{label}' because the dropdown remained {state} within "
                f"{editable_timeout_seconds} seconds. Container HTML: {container_html}"
            )
            return False

        return DropdownUtils.__selectDropdownValueByCombobox(
            page,
            combobox,
            normalized_value,
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
        option = DropdownUtils.__waitForVisibleComponent(
            page,
            option_locators,
            timeout_seconds=option_timeout_seconds,
            poll_interval_seconds=poll_interval_seconds,
        )

        return option is not None

    @staticmethod
    def waitForLabeledValueToLoad(
        page: Page,
        label: str,
        timeout_seconds: int = 5,
        poll_interval_seconds: int = 1,
    ) -> bool:
        """Wait for a labeled dropdown-related field to show a non-empty value."""
        container = DropdownUtils.__ensureComponentVisible(
            DropdownUtils.__findLabeledContainer(page, label),
            label,
            "field container",
        )
        poll_interval_ms = max(poll_interval_seconds * 1000, 100)
        deadline = time.monotonic() + timeout_seconds

        while time.monotonic() < deadline:
            try:
                fields = container.locator(
                    'input:not([type="hidden"]), textarea, [role="combobox"]'
                )
                for index in range(fields.count()):
                    field = fields.nth(index)
                    if not field.is_visible():
                        continue

                    try:
                        loaded_value = field.input_value().strip()
                    except Exception:
                        loaded_value = " ".join(field.inner_text().split()).strip()

                    if loaded_value:
                        return True

                container_text = " ".join(container.inner_text().split())
                if container_text and container_text.casefold() != label.strip().casefold():
                    return True
            except Exception:
                pass

            page.wait_for_timeout(poll_interval_ms)

        print(
            f"Skipping wait for '{label}' because no value was loaded within "
            f"{timeout_seconds} seconds."
        )
        return False
