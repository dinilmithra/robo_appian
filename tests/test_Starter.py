import os
import re

import pytest
from playwright.sync_api import Page

from robo_appian.components.ButtonUtils import ButtonUtils
from robo_appian.components.DropdownUtils import DropdownUtils
from robo_appian.components.SearchDropdownUtils import SearchDropdownUtils
from robo_appian.components.InputUtils import InputUtils
from robo_appian.components.SearchInputUtils import SearchInputUtils
from robo_appian.utils.ComponentUtils import ComponentUtils

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


def _create_request(
    page: Page,
    editable_timeout_seconds: int,
    poll_interval_seconds: int,
) -> None:

    ComponentUtils.waitForElementToBeVisibleByText(page, "Create Request")

    DropdownUtils.selectDropdownIfEditable(
        page,
        "Phase",
        "Execution",
        editable_timeout_seconds=editable_timeout_seconds,
        poll_interval_seconds=int(poll_interval_seconds),
    )
    DropdownUtils.selectDropdownIfEditable(
        page,
        "Request Category",
        "P-Card",
        editable_timeout_seconds=editable_timeout_seconds,
        poll_interval_seconds=int(poll_interval_seconds),
    )
    DropdownUtils.selectDropdownIfEditable(
        page,
        "Request Sub-Category",
        "Convenience Check",
        editable_timeout_seconds=editable_timeout_seconds,
        poll_interval_seconds=int(poll_interval_seconds),
    )
    DropdownUtils.selectDropdownIfEditable(
        page,
        "Fiscal Year",
        "2026",
        editable_timeout_seconds=editable_timeout_seconds,
        poll_interval_seconds=int(poll_interval_seconds),
    )
    SearchInputUtils.select(
        page,
        "Entity Lookup",
        "FDA/CDER/OSP/OPSA/DSAS/",
    )

    DropdownUtils.waitForLabeledValueToLoad(
        page,
        "Center",
        timeout_seconds=editable_timeout_seconds,
        poll_interval_seconds=int(poll_interval_seconds),
    )

    ButtonUtils.click(page)


def _request_details_tab(
    page: Page,
    editable_timeout_seconds: int,
    poll_interval_seconds: int,
) -> None:
    InputUtils.fill_value(
        page,
        "Title*",
        "Selenium Testcase",
    )
    InputUtils.fill_value(
        page,
        "Description/Justification*",
        "Selenium Testcase",
    )
    InputUtils.fill_value(
        page,
        "Purchase Amount *",
        "600",
    )
    InputUtils.fill_value(
        page,
        "Check Issued Date",
        "04/05/2026",
    )
    InputUtils.fill_value(
        page,
        "Check #",
        "123456789",
    )
    DropdownUtils.selectDropdownIfEditable(
        page,
        "P-Card Holder",
        "Bala Chikkala - 676767",
        editable_timeout_seconds=editable_timeout_seconds,
        poll_interval_seconds=int(poll_interval_seconds),
    )
    SearchDropdownUtils.selectSearchDropdownValueIfEditable(
        page,
        "Order Type*",
        "Office Supplies",
    )
    SearchInputUtils.select(
        page,
        "Vendor Name*",
        "GUIDEHOUSE INC.",
    )
    InputUtils.fill_value(
        page,
        "Vendor Address",
        "GUIDEHOUSE INC.",
    )
    InputUtils.fill_value(
        page,
        "Date Purchased",
        "04/05/2026",
    )
    DropdownUtils.selectDropdownIfEditable(
        page,
        "Required Source",
        "No",
        editable_timeout_seconds=editable_timeout_seconds,
        poll_interval_seconds=int(poll_interval_seconds),
    )
    InputUtils.fill_value(
        page,
        "Source Justification",
        "Selenium Testcase",
    )


def test_starter(page: Page) -> None:
    """Starter workflow generated from `test_cases/starter.md` using Playwright only."""
    editable_timeout_seconds = int(os.getenv("EDITABLE_CHECK_TIMEOUT_SECONDS", "20"))
    poll_interval_seconds = int(os.getenv("POLL_INTERVAL_SECONDS", "1"))

    _open_new_request(page)
    _create_request(page, editable_timeout_seconds, poll_interval_seconds)
    _request_details_tab(page, editable_timeout_seconds, poll_interval_seconds)
