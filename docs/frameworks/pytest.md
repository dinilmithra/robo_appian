# pytest Integration

Use Playwright fixtures and keep robo_appian calls page-first.

## Example
```python
import pytest
from playwright.sync_api import sync_playwright
from robo_appian import ButtonUtils, InputUtils

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        yield browser
        browser.close()

@pytest.fixture
def page(browser):
    context = browser.new_context()
    page = context.new_page()
    page.set_default_timeout(15000)
    yield page
    context.close()

def test_login(page):
    page.goto("https://your-appian.example.com")
    InputUtils.setValueByLabelText(page, "Username", "demo")
    ButtonUtils.clickByLabelText(page, "Sign In")
```
