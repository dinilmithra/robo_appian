# Using Robo Appian with Pytest

This page explains how to use Robo Appian in your Pytest-based test suites.

## Installation

Make sure you have `pytest`, `selenium`, and `robo_appian` installed:

```bash
pip install pytest selenium robo_appian
```

## Example: Basic Pytest Test

```python
import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from robo_appian.components.InputUtils import InputUtils
from robo_appian.components.ButtonUtils import ButtonUtils

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

def test_login(driver):
    wait = WebDriverWait(driver, 10)
    driver.get("https://your-appian-app.com")
    InputUtils.setValueByLabelText(wait, "Username", "test_user")
    InputUtils.setValueByLabelText(wait, "Password", "password123")
    ButtonUtils.clickByLabelText(wait, "Sign In")
    # Add assertions here
```

## Tips
- Use fixtures to manage WebDriver setup/teardown
- Use assertions to validate outcomes
- Integrate with CI/CD for automated test runs
