import re
from typing import Any

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

Page = Any
Locator = Any


class SearchDropdownUtils:
    """Playwright helper for selecting Appian search dropdown values only when editable."""

    @staticmethod
    def __exactTextPattern(text: str) -> re.Pattern[str]:
        return re.compile(rf"^\s*{re.escape(text)}\s*$", re.IGNORECASE)

    @staticmethod
    def __partialTextPattern(text: str) -> re.Pattern[str]:
        return re.compile(re.escape(text.strip()), re.IGNORECASE)

    @staticmethod
    def __findLabelElement(page: Page, label: str) -> Locator:
        exact_match = page.locator("label, span").filter(
            has_text=SearchDropdownUtils.__exactTextPattern(label)
        ).first
        if exact_match.count() > 0:
            return exact_match

        return page.locator("label, span").filter(
            has_text=SearchDropdownUtils.__partialTextPattern(label)
        ).first

    @staticmethod
    def __findControlByLabel(page: Page, label: str) -> Locator | None:
        label_element = SearchDropdownUtils.__findLabelElement(page, label)
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
        label_element = SearchDropdownUtils.__findLabelElement(page, label)
        if label_element.count() > 0:
            container = label_element.locator(
                "xpath=ancestor::div[@role='presentation'][1]"
            ).first
            if container.count() > 0:
                return container

        label_pattern = SearchDropdownUtils.__exactTextPattern(label)
        return page.locator("div[role='presentation']").filter(
            has=page.locator("label, span").filter(has_text=label_pattern)
        ).first

    @staticmethod
    def __findSearchDropdown(page: Page, label: str) -> Locator:
        exact_role_match = page.get_by_role(
            "combobox",
            name=SearchDropdownUtils.__exactTextPattern(label),
        ).first
        if exact_role_match.count() > 0:
            return exact_role_match

        partial_role_match = page.get_by_role(
            "combobox",
            name=SearchDropdownUtils.__partialTextPattern(label),
        ).first
        if partial_role_match.count() > 0:
            return partial_role_match

        control = SearchDropdownUtils.__findControlByLabel(page, label)
        if control is not None:
            if control.get_attribute("role") == "combobox":
                return control

            parent_combobox = control.locator(
                "xpath=ancestor-or-self::*[@role='combobox'][1]"
            ).first
            if parent_combobox.count() > 0:
                return parent_combobox

        return SearchDropdownUtils.__findLabeledContainer(page, label).locator(
            'div[role="combobox"], input[role="combobox"]'
        ).first

    @staticmethod
    def __getFillableInput(search_dropdown: Locator, page: Page) -> tuple[Locator, str | None]:
        component_id = search_dropdown.get_attribute("id")
        if component_id and component_id.endswith("_value"):
            base_component_id = component_id[: -len("_value")]
            return page.locator(f'[id="{base_component_id}_searchInput"]').first, component_id

        return search_dropdown, component_id

    @staticmethod
    def __getOptionCandidates(
        page: Page,
        search_dropdown: Locator,
        fillable_input: Locator,
        value: str,
        component_id: str | None,
    ) -> list[Locator]:
        dropdown_list_id = (
            fillable_input.get_attribute("aria-controls")
            or search_dropdown.get_attribute("aria-controls")
        )
        if not dropdown_list_id and component_id and component_id.endswith("_value"):
            dropdown_list_id = f'{component_id[: -len("_value")]}_list'

        option_candidates: list[Locator] = []
        if dropdown_list_id:
            scoped_options = page.locator(
                f'ul[id="{dropdown_list_id}"] li, [id="{dropdown_list_id}"] [role="option"]'
            )
            option_candidates.extend(
                [
                    scoped_options.filter(
                        has_text=SearchDropdownUtils.__exactTextPattern(value)
                    ).first,
                    scoped_options.filter(
                        has_text=SearchDropdownUtils.__partialTextPattern(value)
                    ).first,
                ]
            )

        option_candidates.extend(
            [
                page.get_by_role(
                    "option",
                    name=SearchDropdownUtils.__exactTextPattern(value),
                ).first,
                page.get_by_role(
                    "option",
                    name=SearchDropdownUtils.__partialTextPattern(value),
                ).first,
            ]
        )
        return option_candidates

    @staticmethod
    def selectSearchDropdownValueIfEditable(
        page: Page,
        label: str,
        value: str,
    ) -> bool:
        """Select a search dropdown value using Playwright's default waiting behavior."""
        normalized_value = "" if value is None else str(value).strip()
        if not normalized_value:
            print(f"Skipping '{label}' because no search dropdown value was provided.")
            return False

        search_dropdown = SearchDropdownUtils.__findSearchDropdown(page, label)
        search_dropdown.click()

        fillable_input, component_id = SearchDropdownUtils.__getFillableInput(
            search_dropdown,
            page,
        )

        fillable_input.click()
        try:
            fillable_input.press("Control+A")
            fillable_input.press("Backspace")
            fillable_input.type(normalized_value, delay=50)
        except Exception:
            fillable_input.fill("")
            fillable_input.fill(normalized_value)

        for option in SearchDropdownUtils.__getOptionCandidates(
            page,
            search_dropdown,
            fillable_input,
            normalized_value,
            component_id,
        ):
            try:
                option.click()
                return True
            except PlaywrightTimeoutError:
                continue

        fillable_input.press("ArrowDown")
        fillable_input.press("Enter")
        return True
