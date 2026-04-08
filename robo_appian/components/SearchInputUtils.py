import re
import time
from typing import Any

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

Page = Any
Locator = Any


class SearchInputUtils:
    """Playwright helper for selecting Appian search input values only when editable."""

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
            has_text=SearchInputUtils.__exactTextPattern(label)
        ).first
        if exact_match.count() > 0:
            return SearchInputUtils.__ensureComponentVisible(exact_match, label, "label")

        partial_match = page.locator("label, span").filter(
            has_text=SearchInputUtils.__partialTextPattern(label)
        ).first
        return SearchInputUtils.__ensureComponentVisible(partial_match, label, "label")

    @staticmethod
    def __findControlByLabel(page: Page, label: str) -> Locator | None:
        label_element = SearchInputUtils.__findLabelElement(page, label)
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
        label_element = SearchInputUtils.__findLabelElement(page, label)
        if label_element.count() > 0:
            container = label_element.locator(
                "xpath=ancestor::div[@role='presentation'][1]"
            ).first
            if container.count() > 0:
                return container

        label_pattern = SearchInputUtils.__exactTextPattern(label)
        return page.locator("div[role='presentation']").filter(
            has=page.locator("label, span").filter(has_text=label_pattern)
        ).first

    @staticmethod
    def __findSearchInput(page: Page, label: str) -> Locator:
        exact_role_match = page.get_by_role(
            "combobox",
            name=SearchInputUtils.__exactTextPattern(label),
        ).first
        if exact_role_match.count() > 0:
            return exact_role_match

        partial_role_match = page.get_by_role(
            "combobox",
            name=SearchInputUtils.__partialTextPattern(label),
        ).first
        if partial_role_match.count() > 0:
            return partial_role_match

        control = SearchInputUtils.__findControlByLabel(page, label)
        if control is not None:
            return control

        container = SearchInputUtils.__findLabeledContainer(page, label)
        visible_search_input = container.locator(
            '[role="combobox"]:visible, '
            'input[id$="_searchInput"]:visible, '
            'input[type="text"]:visible, '
            'textarea:visible'
        ).first
        if visible_search_input.count() > 0:
            return visible_search_input

        return container.locator(
            '[role="combobox"], input[id$="_searchInput"], input[type="text"], textarea'
        ).first

    @staticmethod
    def __isInputEditable(input_component: Locator) -> bool:
        try:
            return (
                input_component.count() > 0
                and input_component.is_visible()
                and input_component.get_attribute("readonly") is None
                and input_component.get_attribute("aria-disabled") != "true"
                and not input_component.is_disabled()
            )
        except Exception:
            return False

    @staticmethod
    def __waitUntilInputEditable(
        page: Page,
        label: str,
        timeout_seconds: int = 20,
        poll_interval_seconds: int = 1,
    ) -> Locator:
        search_input = SearchInputUtils.__ensureComponentVisible(
            SearchInputUtils.__findSearchInput(page, label),
            label,
            "search input",
        )
        poll_interval_ms = int(poll_interval_seconds * 1000)
        deadline = time.monotonic() + timeout_seconds

        while time.monotonic() < deadline:
            if SearchInputUtils.__isInputEditable(search_input):
                return search_input
            page.wait_for_timeout(poll_interval_ms)

        return search_input

    @staticmethod
    def __trySelectSearchResult(
        page: Page,
        search_input: Locator,
        fillable_input: Locator,
        value: str,
        timeout_ms: int,
    ) -> bool:
        dropdown_list_id = (
            fillable_input.get_attribute("aria-controls")
            or search_input.get_attribute("aria-controls")
        )

        option_locators: list[Locator] = []
        if dropdown_list_id:
            option_locators.append(
                page.locator(
                    f'ul[id="{dropdown_list_id}"] li, '
                    f'[id="{dropdown_list_id}"] [role="option"]'
                ).filter(has_text=SearchInputUtils.__partialTextPattern(value)).first
            )

        option_locators.append(
            page.get_by_role("option", name=SearchInputUtils.__partialTextPattern(value)).first
        )
        option_locators.append(
            page.locator('[role="option"], li').filter(
                has_text=SearchInputUtils.__partialTextPattern(value)
            ).first
        )

        deadline = time.monotonic() + (timeout_ms / 1000)
        while time.monotonic() < deadline:
            for option in option_locators:
                try:
                    if option.count() == 0 or not option.is_visible():
                        continue
                    option.scroll_into_view_if_needed()
                    option.click()
                    page.wait_for_timeout(500)
                    return True
                except Exception:
                    continue
            page.wait_for_timeout(200)

        return False

    @staticmethod
    def __waitForLabeledValueToLoad(
        page: Page,
        label: str,
        timeout_seconds: int,
        poll_interval_seconds: int,
    ) -> bool:
        container = SearchInputUtils.__ensureComponentVisible(
            SearchInputUtils.__findLabeledContainer(page, label),
            label,
            "field container",
        )
        poll_interval_ms = int(poll_interval_seconds * 1000)
        deadline = time.monotonic() + timeout_seconds

        while time.monotonic() < deadline:
            try:
                inputs = container.locator(
                    'input:not([type="hidden"]), textarea, [role="combobox"]'
                )
                for index in range(inputs.count()):
                    field = inputs.nth(index)
                    if not field.is_visible():
                        continue

                    try:
                        loaded_value = field.input_value().strip()
                    except Exception:
                        loaded_value = field.inner_text().strip()

                    if loaded_value:
                        return True

                container_text = " ".join(container.inner_text().split())
                if container_text and container_text.casefold() != label.strip().casefold():
                    return True
            except Exception:
                pass

            page.wait_for_timeout(poll_interval_ms)

        return False

    @staticmethod
    def selectSearchInputValueIfEditable(
        page: Page,
        label: str,
        value: str,
        editable_timeout_seconds: int = 5,
        poll_interval_seconds: int = 1,
    ) -> bool:
        """Select a search input value after waiting for the labeled input to become editable."""
        search_input = SearchInputUtils.__waitUntilInputEditable(
            page,
            label,
            timeout_seconds=editable_timeout_seconds,
            poll_interval_seconds=poll_interval_seconds,
        )
        if not SearchInputUtils.__isInputEditable(search_input):
            print(
                f"Skipping '{label}' because the search input is not editable within "
                f"{editable_timeout_seconds} seconds."
            )
            return False

        fillable_input = search_input
        tag_name = search_input.evaluate("element => element.tagName.toLowerCase()")
        if tag_name not in {"input", "textarea"}:
            nested_input = search_input.locator('input:visible, textarea:visible').first
            if nested_input.count() > 0:
                fillable_input = SearchInputUtils.__ensureComponentVisible(
                    nested_input,
                    label,
                    "search input",
                )

        deadline = time.monotonic() + editable_timeout_seconds
        poll_interval_ms = int(poll_interval_seconds * 1000)

        while time.monotonic() < deadline:
            fillable_input.click()
            try:
                fillable_input.press("Control+A")
                fillable_input.press("Backspace")
                fillable_input.type(value, delay=50)
            except Exception:
                fillable_input.fill("")
                fillable_input.fill(value)

            page.wait_for_timeout(750)

            remaining_ms = max(int((deadline - time.monotonic()) * 1000), 250)
            option_timeout_ms = min(max(poll_interval_ms * 2, 1500), remaining_ms)
            if SearchInputUtils.__trySelectSearchResult(
                page,
                search_input,
                fillable_input,
                value,
                option_timeout_ms,
            ):
                return True

            fillable_input.press("ArrowDown")
            page.wait_for_timeout(250)
            fillable_input.press("Enter")
            page.wait_for_timeout(750)

            if label.strip().casefold() == "entity lookup" and SearchInputUtils.__waitForLabeledValueToLoad(
                page,
                "Center",
                timeout_seconds=2,
                poll_interval_seconds=min(poll_interval_seconds, 1),
            ):
                return True

        print(
            f"Skipping '{label}' because search result '{value}' was not available in time."
        )
        return False

    @staticmethod
    def selectSearchInputByLabelText(page: Page, label: str, value: str) -> Locator:
        """Select a value in a search input by label text."""
        SearchInputUtils.selectSearchInputValueIfEditable(page, label, value)
        return SearchInputUtils.__findSearchInput(page, label)

    @staticmethod
    def selectSearchInputByPartialLabelText(page: Page, label: str, value: str) -> Locator:
        """Select a value in a search input by partial label text."""
        SearchInputUtils.selectSearchInputValueIfEditable(page, label, value)
        return SearchInputUtils.__findSearchInput(page, label)

    @staticmethod
    def selectSearchDropdownByLabelText(page: Page, label: str, value: str) -> Locator:
        """Select a value in a search dropdown by label text."""
        return SearchInputUtils.selectSearchInputByLabelText(page, label, value)

    @staticmethod
    def selectSearchDropdownByPartialLabelText(page: Page, label: str, value: str) -> Locator:
        """Select a value in a search dropdown by partial label text."""
        return SearchInputUtils.selectSearchInputByPartialLabelText(page, label, value)
