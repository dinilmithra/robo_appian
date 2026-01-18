# Your First Test

This walkthrough creates a basic login test that you can adapt for your Appian environment.

## Project skeleton
```
project/
├─ tests/
│  └─ test_login.py
└─ conftest.py (optional for driver fixtures)
```

## Example pytest fixture (optional)
```python
# conftest.py
import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

@pytest.fixture
def wait():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield WebDriverWait(driver, 10)
    driver.quit()
```

## Test: login by labels
```python
# tests/test_login.py
from robo_appian.components import InputUtils, ButtonUtils
from robo_appian.utils.ComponentUtils import ComponentUtils

APP_URL = "https://your-appian.example.com"


def test_user_can_login(wait):
    driver = wait._driver
    driver.get(APP_URL)

    InputUtils.setValueByLabelText(wait, "Username", "demo_user")
    InputUtils.setValueByLabelText(wait, "Password", "SuperSecret!")
    ButtonUtils.clickByLabelText(wait, "Sign In")

    # Assert a post-login label is visible
    ComponentUtils.waitForElementToBeVisibleByText(wait, "Welcome")
```

## Running tests
```bash
pytest -q
```

If you prefer `unittest`, see [unittest integration](../frameworks/unittest.md).
