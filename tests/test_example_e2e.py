import os
import pytest

from robo_appian.components.InputUtils import InputUtils
from robo_appian.components.ButtonUtils import ButtonUtils
from robo_appian.components.LabelUtils import LabelUtils
from robo_appian.controllers.ComponentDriver import ComponentDriver


@pytest.mark.e2e
def test_example_login_flow(driver, wait, app_url):
    """
    Minimal example showing the recommended wait-first patterns and ComponentDriver.

    This test is illustrative and will only run if RUN_E2E=1 and APP_URL is set.
    It assumes the target page has an input labeled "Username" and a button labeled
    "Sign In". Adjust labels to match your Appian environment.
    """
    if os.getenv("RUN_E2E") != "1":
        pytest.skip("RUN_E2E!=1; skipping example e2e test.")

    driver.get(app_url)

    # Direct utility usage (preferred low-level pattern)
    InputUtils.setValueByLabelText(wait, "Username", "testuser")
    ButtonUtils.clickByLabelText(wait, "Sign In")

    # Orchestrated action via router (preferred high-level pattern)
    ComponentDriver.execute(wait, "Input Text", "Set Value", "Username", "testuser")
    ComponentDriver.execute(wait, "Button", "Click", "Sign In", None)

    # Example assertion: ensure a label appears after sign-in (adjust to your app)
    assert LabelUtils.isLabelExistsAfterLoad(wait, "Welcome") is True
