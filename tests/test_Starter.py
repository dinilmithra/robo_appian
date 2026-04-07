import os
import re
import time

import pytest
from playwright.sync_api import Locator, Page, TimeoutError as PlaywrightTimeoutError

from robo_appian.components.DropdownHelper import DropdownHelper

pytestmark = pytest.mark.e2e


def _exact_text_pattern(text: str) -> re.Pattern[str]:
    return re.compile(rf"^\s*{re.escape(text)}\s*$", re.IGNORECASE)


def _partial_text_pattern(text: str) -> re.Pattern[str]:
    return re.compile(re.escape(text.strip()), re.IGNORECASE)


def _open_new_request(page: Page) -> None:
    page.get_by_role(
        "link",
        name=_exact_text_pattern("Create a New Request"),
    ).first.click()
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_load_state("networkidle")


def _ensure_component_visible(
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


def _find_label_element(page: Page, label: str) -> Locator:
    exact_pattern = _exact_text_pattern(label)
    exact_match = page.locator("label, span").filter(has_text=exact_pattern).first
    if exact_match.count() > 0:
        return _ensure_component_visible(exact_match, label, "label")

    partial_match = page.locator("label, span").filter(
        has_text=_partial_text_pattern(label)
    ).first
    return _ensure_component_visible(partial_match, label, "label")


def _find_control_by_label(page: Page, label: str) -> Locator | None:
    label_element = _find_label_element(page, label)
    if label_element.count() == 0:
        return None

    control_id = label_element.get_attribute("for")
    if not control_id:
        return None

    control = page.locator(f'[id="{control_id}"]').first
    if control.count() == 0:
        return None

    return control


def _find_labeled_container(page: Page, label: str) -> Locator:
    label_element = _find_label_element(page, label)
    if label_element.count() > 0:
        container = label_element.locator(
            "xpath=ancestor::div[@role='presentation'][1]"
        ).first
        if container.count() > 0:
            return container

    label_pattern = _exact_text_pattern(label)
    return page.locator("div[role='presentation']").filter(
        has=page.locator("label, span").filter(has_text=label_pattern)
    ).first


def _find_combobox(page: Page, label: str) -> Locator:
    exact_role_match = page.get_by_role("combobox", name=_exact_text_pattern(label)).first
    if exact_role_match.count() > 0:
        return exact_role_match

    partial_role_match = page.get_by_role(
        "combobox",
        name=_partial_text_pattern(label),
    ).first
    if partial_role_match.count() > 0:
        return partial_role_match

    control = _find_control_by_label(page, label)
    if control is not None:
        if control.get_attribute("role") == "combobox":
            return control

        parent_combobox = control.locator(
            "xpath=ancestor-or-self::*[@role='combobox'][1]"
        ).first
        if parent_combobox.count() > 0:
            return parent_combobox

    return _find_labeled_container(page, label).locator(
        'div[role="combobox"], input[role="combobox"]'
    ).first


def _find_search_input(page: Page, label: str) -> Locator:
    exact_role_match = page.get_by_role("combobox", name=_exact_text_pattern(label)).first
    if exact_role_match.count() > 0:
        return exact_role_match

    partial_role_match = page.get_by_role(
        "combobox",
        name=_partial_text_pattern(label),
    ).first
    if partial_role_match.count() > 0:
        return partial_role_match

    control = _find_control_by_label(page, label)
    if control is not None:
        return control

    container = _find_labeled_container(page, label)
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


def _find_search_dropdown(page: Page, label: str) -> Locator:
    return _find_combobox(page, label)


def _find_text_input(page: Page, label: str) -> Locator:
    control = _find_control_by_label(page, label)
    if control is not None:
        return control

    return _find_labeled_container(page, label).locator(
        'input:not([id$="_searchInput"]):not([type="hidden"]), textarea'
    ).first


def _is_input_editable(input_component: Locator) -> bool:
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


def _is_dropdown_editable(combobox: Locator) -> bool:
    try:
        return (
            combobox.count() > 0
            and combobox.is_visible()
            and combobox.get_attribute("aria-disabled") != "true"
            and not combobox.is_disabled()
        )
    except Exception:
        return False


def _wait_until_dropdown_editable(
    page: Page,
    label: str,
    timeout_seconds: int,
    poll_interval_seconds: float,
) -> Locator:
    poll_interval_ms = int(poll_interval_seconds * 1000)
    combobox = _ensure_component_visible(_find_combobox(page, label), label, "dropdown")
    deadline = time.monotonic() + timeout_seconds

    while time.monotonic() < deadline:
        if _is_dropdown_editable(combobox):
            return combobox
        page.wait_for_timeout(poll_interval_ms)

    return combobox


def _wait_until_input_editable(
    page: Page,
    label: str,
    timeout_seconds: int,
    poll_interval_seconds: float,
) -> Locator:
    search_input = _ensure_component_visible(
        _find_search_input(page, label),
        label,
        "search input",
    )
    poll_interval_ms = int(poll_interval_seconds * 1000)
    deadline = time.monotonic() + timeout_seconds

    while time.monotonic() < deadline:
        if _is_input_editable(search_input):
            return search_input
        page.wait_for_timeout(poll_interval_ms)

    return search_input


def _wait_until_search_dropdown_editable(
    page: Page,
    label: str,
    timeout_seconds: int,
    poll_interval_seconds: float,
) -> Locator:
    search_dropdown = _ensure_component_visible(
        _find_search_dropdown(page, label),
        label,
        "search dropdown",
    )
    poll_interval_ms = int(poll_interval_seconds * 1000)
    deadline = time.monotonic() + timeout_seconds

    while time.monotonic() < deadline:
        if _is_input_editable(search_dropdown) or _is_dropdown_editable(search_dropdown):
            return search_dropdown
        page.wait_for_timeout(poll_interval_ms)

    return search_dropdown


def _wait_until_text_input_editable(
    page: Page,
    label: str,
    timeout_seconds: int,
    poll_interval_seconds: float,
) -> Locator:
    text_input = _ensure_component_visible(
        _find_text_input(page, label),
        label,
        "text input",
    )
    poll_interval_ms = int(poll_interval_seconds * 1000)
    deadline = time.monotonic() + timeout_seconds

    while time.monotonic() < deadline:
        if _is_input_editable(text_input):
            return text_input
        page.wait_for_timeout(poll_interval_ms)

    return text_input


def _try_select_search_result(
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
            ).filter(has_text=_partial_text_pattern(value)).first
        )

    option_locators.append(
        page.get_by_role("option", name=_partial_text_pattern(value)).first
    )
    option_locators.append(
        page.locator('[role="option"], li').filter(
            has_text=_partial_text_pattern(value)
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


def _select_search_input_value_if_editable(
    page: Page,
    label: str,
    value: str,
    editable_timeout_seconds: int,
    poll_interval_seconds: float,
) -> bool:
    poll_interval_ms = int(poll_interval_seconds * 1000)
    search_input = _wait_until_input_editable(
        page,
        label,
        timeout_seconds=editable_timeout_seconds,
        poll_interval_seconds=poll_interval_seconds,
    )
    if not _is_input_editable(search_input):
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
            fillable_input = _ensure_component_visible(
                nested_input,
                label,
                "search input",
            )

    deadline = time.monotonic() + editable_timeout_seconds

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
        if _try_select_search_result(
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

        if label.strip().casefold() == "entity lookup" and _wait_for_labeled_value_to_load(
            page,
            "Center",
            timeout_seconds=2,
            poll_interval_seconds=min(poll_interval_seconds, 0.25),
        ):
            return True

    print(
        f"Skipping '{label}' because search result '{value}' was not available in time."
    )
    return False


def _select_search_dropdown_value_if_editable(
    page: Page,
    label: str,
    value: str,
    editable_timeout_seconds: int,
    poll_interval_seconds: float,
) -> bool:
    poll_interval_ms = int(poll_interval_seconds * 1000)
    search_dropdown = _wait_until_search_dropdown_editable(
        page,
        label,
        timeout_seconds=editable_timeout_seconds,
        poll_interval_seconds=poll_interval_seconds,
    )
    if not (_is_input_editable(search_dropdown) or _is_dropdown_editable(search_dropdown)):
        print(
            f"Skipping '{label}' because the search dropdown is not editable within "
            f"{editable_timeout_seconds} seconds."
        )
        return False

    search_dropdown.click()

    component_id = search_dropdown.get_attribute("id")
    fillable_input = search_dropdown
    if component_id and component_id.endswith("_value"):
        base_component_id = component_id[: -len("_value")]
        linked_input = page.locator(f'[id="{base_component_id}_searchInput"]').first
        fillable_input = _ensure_component_visible(linked_input, label, "search input")

    fillable_input.click()
    try:
        fillable_input.press("Control+A")
        fillable_input.press("Backspace")
        fillable_input.type(value, delay=50)
    except Exception:
        fillable_input.fill(value)
    page.wait_for_timeout(500)

    dropdown_list_id = (
        fillable_input.get_attribute("aria-controls")
        or search_dropdown.get_attribute("aria-controls")
    )
    if not dropdown_list_id and component_id and component_id.endswith("_value"):
        dropdown_list_id = f'{component_id[: -len("_value")]}_list'

    if dropdown_list_id:
        option = page.locator(
            f'ul[id="{dropdown_list_id}"] li, [id="{dropdown_list_id}"] [role="option"]'
        ).filter(has_text=_partial_text_pattern(value)).first
        try:
            option.wait_for(state="visible", timeout=editable_timeout_seconds * 1000)
            option.click()
            page.wait_for_timeout(250)
            return True
        except PlaywrightTimeoutError:
            pass

    fillable_input.press("ArrowDown")
    fillable_input.press("Enter")
    page.wait_for_timeout(250)
    return True


def _fill_text_input_if_editable(
    page: Page,
    label: str,
    value: str,
    editable_timeout_seconds: int,
    poll_interval_seconds: float,
) -> bool:
    poll_interval_ms = int(poll_interval_seconds * 1000)
    text_input = _wait_until_text_input_editable(
        page,
        label,
        timeout_seconds=editable_timeout_seconds,
        poll_interval_seconds=poll_interval_seconds,
    )
    if not _is_input_editable(text_input):
        print(
            f"Skipping '{label}' because the text input is not editable within "
            f"{editable_timeout_seconds} seconds."
        )
        return False

    text_input.click()
    text_input.fill(value)
    page.wait_for_timeout(250)
    return True


def _wait_for_labeled_value_to_load(
    page: Page,
    label: str,
    timeout_seconds: int,
    poll_interval_seconds: float,
) -> bool:
    container = _ensure_component_visible(
        _find_labeled_container(page, label),
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
                    value = field.input_value().strip()
                except Exception:
                    value = field.inner_text().strip()

                if value:
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


def _click_submit(
    page: Page,
    timeout_seconds: int,
    poll_interval_seconds: float,
) -> None:
    submit_button = page.get_by_role(
        "button",
        name=_exact_text_pattern("Submit"),
    ).first
    submit_button.wait_for(state="visible")

    effective_timeout_seconds = max(timeout_seconds, 15)
    poll_interval_ms = int(poll_interval_seconds * 1000)
    deadline = time.monotonic() + effective_timeout_seconds
    while time.monotonic() < deadline:
        if not submit_button.is_disabled():
            submit_button.scroll_into_view_if_needed()
            submit_button.click()
            return
        page.wait_for_timeout(poll_interval_ms)

    raise AssertionError(
        f"Expected 'Submit' button to become enabled within {effective_timeout_seconds} seconds, but it remained disabled."
    )


def _create_request(
    page: Page,
    editable_timeout_seconds: int,
    poll_interval_seconds: float,
) -> None:
    DropdownHelper.selectDropdownIfEditable(
        page,
        "Phase",
        "Execution",
        editable_timeout_seconds=editable_timeout_seconds,
        poll_interval_seconds=poll_interval_seconds,
    )
    DropdownHelper.selectDropdownIfEditable(
        page,
        "Request Category",
        "P-Card",
        editable_timeout_seconds=editable_timeout_seconds,
        poll_interval_seconds=poll_interval_seconds,
    )
    DropdownHelper.selectDropdownIfEditable(
        page,
        "Request Sub-Category",
        "Convenience Check",
        editable_timeout_seconds=editable_timeout_seconds,
        poll_interval_seconds=poll_interval_seconds,
    )
    DropdownHelper.selectDropdownIfEditable(
        page,
        "Fiscal Year",
        "2026",
        editable_timeout_seconds=editable_timeout_seconds,
        poll_interval_seconds=poll_interval_seconds,
    )
    _select_search_input_value_if_editable(
        page,
        "Entity Lookup",
        "FDA/CDER/OSP/OPSA/DSAS/",
        editable_timeout_seconds=editable_timeout_seconds,
        poll_interval_seconds=poll_interval_seconds,
    )
    _wait_for_labeled_value_to_load(
        page,
        "Center",
        timeout_seconds=editable_timeout_seconds,
        poll_interval_seconds=poll_interval_seconds,
    )
    _click_submit(page, editable_timeout_seconds, poll_interval_seconds)


def _request_details_tab(
    page: Page,
    editable_timeout_seconds: int,
    poll_interval_seconds: float,
) -> None:
    _fill_text_input_if_editable(
        page,
        "Title*",
        "Selenium Testcase",
        editable_timeout_seconds=editable_timeout_seconds,
        poll_interval_seconds=poll_interval_seconds,
    )
    _fill_text_input_if_editable(
        page,
        "Description/Justification*",
        "Selenium Testcase",
        editable_timeout_seconds=editable_timeout_seconds,
        poll_interval_seconds=poll_interval_seconds,
    )
    _fill_text_input_if_editable(
        page,
        "Purchase Amount *",
        "600",
        editable_timeout_seconds=editable_timeout_seconds,
        poll_interval_seconds=poll_interval_seconds,
    )
    _fill_text_input_if_editable(
        page,
        "Check Issued Date",
        "04/05/2026",
        editable_timeout_seconds=editable_timeout_seconds,
        poll_interval_seconds=poll_interval_seconds,
    )
    _fill_text_input_if_editable(
        page,
        "Check #",
        "123456789",
        editable_timeout_seconds=editable_timeout_seconds,
        poll_interval_seconds=poll_interval_seconds,
    )
    DropdownHelper.selectDropdownIfEditable(
        page,
        "P-Card Holder",
        "Bala Chikkala - 676767",
        editable_timeout_seconds=editable_timeout_seconds,
        poll_interval_seconds=poll_interval_seconds,
    )
    _select_search_dropdown_value_if_editable(
        page,
        "Order Type*",
        "Office Supplies",
        editable_timeout_seconds=editable_timeout_seconds,
        poll_interval_seconds=poll_interval_seconds,
    )
    _select_search_input_value_if_editable(
        page,
        "Vendor Name*",
        "GUIDEHOUSE INC.",
        editable_timeout_seconds=editable_timeout_seconds,
        poll_interval_seconds=poll_interval_seconds,
    )
    _fill_text_input_if_editable(
        page,
        "Vendor Address",
        "GUIDEHOUSE INC.",
        editable_timeout_seconds=editable_timeout_seconds,
        poll_interval_seconds=poll_interval_seconds,
    )
    _fill_text_input_if_editable(
        page,
        "Date Purchased",
        "04/05/2026",
        editable_timeout_seconds=editable_timeout_seconds,
        poll_interval_seconds=poll_interval_seconds,
    )
    DropdownHelper.selectDropdownIfEditable(
        page,
        "Required Source",
        "No",
        editable_timeout_seconds=editable_timeout_seconds,
        poll_interval_seconds=poll_interval_seconds,
    )
    _fill_text_input_if_editable(
        page,
        "Source Justification",
        "Selenium Testcase",
        editable_timeout_seconds=editable_timeout_seconds,
        poll_interval_seconds=poll_interval_seconds,
    )


def test_starter(page: Page) -> None:
    """Starter workflow generated from `test_cases/starter.md` using Playwright only."""
    editable_timeout_seconds = int(os.getenv("EDITABLE_CHECK_TIMEOUT_SECONDS", "20"))
    poll_interval_seconds = float(os.getenv("POLL_INTERVAL_SECONDS", "1"))

    _open_new_request(page)
    _create_request(page, editable_timeout_seconds, poll_interval_seconds)
    _request_details_tab(page, editable_timeout_seconds, poll_interval_seconds)
