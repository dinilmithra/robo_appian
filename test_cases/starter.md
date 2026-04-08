Generate a Playwright + pytest test script named `test_Starter.py` inside the `tests` folder.

Requirements:
- Use Python Playwright sync API only.
- Do not use any `robo_appian` helper classes inside the test.
- Mark the test with `pytest.mark.e2e`.
- Use the existing `page` fixture from `tests/conftest.py`.
- Follow clean Playwright style with small helper methods.

Test flow:
1. Open the Appian page that is already prepared by the `page` fixture.
2. Click the `Create a New Request` link.
3. Wait for the page to finish loading.
4. Select `Execution` from the `Phase` dropdown if the dropdown becomes editable.
5. Select `P-Card` from the `Request Category` dropdown if the dropdown becomes editable.
6. Select `Convenience Check` from the `Request Sub-Category` dropdown if the dropdown becomes editable.
7. Select `2026` from the `Fiscal Year` dropdown if the dropdown becomes editable.
8. Select `FDA/CDER/OSP/OPSA/DSAS/` from the `Entity Lookup` search input component when editable.
9. Wait for content to load in the `Center` field.
10. Click the `Submit` button after it becomes enabled.
11. Fill `Selenium Testcase` into the `Title*` textbox when editable.
12. Fill `Selenium Testcase` into the `Description/Justification*` textbox when editable.
13. Fill `600` into the `Purchase Amount *` textbox when editable.
14. Fill `04/05/2026` into the `Check Issued Date` field when editable.
15. Fill `123456789` into the `Check #` textbox when editable.
16. Select `Bala Chikkala - 676767` from the `P-Card Holder` dropdown when editable.
17. Select `Office Supplies` from the `Order Type*` search dropdown when editable.
18. Fill `GUIDEHOUSE INC.` into the `Vendor Name*` search input when editable.
19. Fill `GUIDEHOUSE INC.` into the `Vendor Address` textbox when editable.
20. Fill `04/05/2026` into the `Date Purchased` field when editable.
21. Select `No` from the `Required Source` dropdown when editable.
22. Fill `Selenium Testcase` into the `Source Justification` textbox when editable.

Implementation details:
- Use regex-based exact text matching for labels and button/link names.
- Add a helper like `_find_combobox(page, label)` for Appian dropdowns using:
  - `div[role='presentation']`
  - nested `span` label text
  - `div[role='combobox']`
- Add `_is_dropdown_editable()` and `_wait_until_dropdown_editable()` helpers.
- Read `EDITABLE_CHECK_TIMEOUT_SECONDS` from environment and use it for the editable wait.
- If a dropdown does not become editable before the configured timeout, skip that dropdown selection and print a message.
- Keep the script simple, readable, and robust.

Return only the full Python code for `tests/test_Starter.py`.