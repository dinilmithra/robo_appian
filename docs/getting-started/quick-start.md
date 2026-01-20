# Quick Start

Get started with Robo Appian in minutes.

## Installation

```bash
pip install robo_appian
```

## Basic Usage

```python
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from robo_appian.components import InputUtils, ButtonUtils

# Setup
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)
driver.get("https://your-appian.example.com")

# Interact by label
InputUtils.setValueByLabelText(wait, "Username", "demo_user")
InputUtils.setValueByLabelText(wait, "Password", "secret")
ButtonUtils.clickByLabelText(wait, "Sign In")

driver.quit()
```

**Key points:**
- Pass `wait` first to all methods
- Components located by visible labels (not IDs)
- Automatic waiting and safe click handling

## With Pytest

```python
# conftest.py
import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

@pytest.fixture
def wait():
    driver = webdriver.Chrome()
    yield WebDriverWait(driver, 10)
    driver.quit()

# test_login.py
def test_login(wait):
    wait._driver.get("https://your-appian.example.com")
    InputUtils.setValueByLabelText(wait, "Username", "demo")
    ButtonUtils.clickByLabelText(wait, "Sign In")
```

## Next Steps
- [Core Components](../user-guide/components.md) - Available utilities
- [Examples](../examples/login.md) - Real-world scenarios
- [API Reference](../api/index.md) - Full documentation
