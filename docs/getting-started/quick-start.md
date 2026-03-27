# Quick Start

Get started with Robo Appian in minutes.

## Installation

```bash
pip install robo_appian
playwright install
```

## Basic Usage

```python
from playwright.sync_api import sync_playwright
from robo_appian.components import InputUtils, ButtonUtils

with sync_playwright() as playwright:
    browser = playwright.chromium.launch()
    page = browser.new_page()
    page.set_default_timeout(10_000)
    page.goto("https://your-appian.example.com")

    InputUtils.setValueByLabelText(page, "Username", "demo_user")
    InputUtils.setValueByLabelText(page, "Password", "secret")
    ButtonUtils.clickByLabelText(page, "Sign In")

    browser.close()
```

**Key points:**
- Pass `page` first to all methods
- Components located by visible labels (not IDs)
- Automatic waiting and safe click handling

## With Pytest

```python
# conftest.py
import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        yield browser
        browser.close()


@pytest.fixture
def page(browser):
    page = browser.new_page()
    page.set_default_timeout(10_000)
    yield page
    page.context.close()

# test_login.py
def test_login(page):
    page.goto("https://your-appian.example.com")
    InputUtils.setValueByLabelText(page, "Username", "demo")
    ButtonUtils.clickByLabelText(page, "Sign In")
```

## Next Steps
- [Core Components](../user-guide/components.md) - Available utilities
- [Examples](../examples/login.md) - Real-world scenarios
- [API Reference](../api/index.md) - Full documentation
