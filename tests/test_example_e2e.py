import os
import pytest

from robo_appian.components.InputUtils import InputUtils
from robo_appian.components.ButtonUtils import ButtonUtils
from robo_appian.components.LabelUtils import LabelUtils


@pytest.mark.e2e
def test_example_login_flow(page, app_url):
    """
    Minimal example showing the recommended page-first patterns.

    This test is illustrative and will only run if RUN_E2E=1 and APP_URL is set.
    It assumes the target page has an input labeled "Username" and a button labeled
    "Sign In". Adjust labels to match your Appian environment.
    """
    if os.getenv("RUN_E2E") != "1":
        pytest.skip("RUN_E2E!=1; skipping example e2e test.")

    page.goto(app_url)

    # Some environments display a consent/accept gate before native login fields.
    accept_button = page.locator("#jsAcceptButton")
    if accept_button.count() > 0 and accept_button.first.is_visible():
        accept_button.first.click()

    native_username = page.locator("#un")
    native_password = page.locator("#pw")
    native_signin = page.locator("#jsLoginButton")

    if native_username.count() > 0 and native_username.first.is_visible():
        username = os.getenv("APP_USERNAME", "testuser")
        password = os.getenv("APP_PASSWORD")

        InputUtils.setValueById(page, "un", username)
        if password:
            InputUtils.setValueById(page, "pw", password)
            ButtonUtils.clickById(page, "jsLoginButton")
            # Credentials and post-login target vary by environment.
            assert "signin=native" not in page.url
            return

        # Selector-level validation for native sign-in page when creds aren't supplied.
        assert native_password.first.is_visible()
        assert native_signin.first.is_visible()
        pytest.skip("APP_PASSWORD not set; validated native login selectors only.")

    # Direct utility usage (preferred low-level pattern)
    InputUtils.setValueByLabelText(page, "Username", "testuser")
    ButtonUtils.clickByLabelText(page, "Sign In")

    # Example assertion: ensure a label appears after sign-in (adjust to your app)
    assert LabelUtils.isLabelExists(page, "Welcome") is True
