# Login Example

```python
from playwright.sync_api import sync_playwright
from robo_appian import ButtonUtils, InputUtils

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()
    page.set_default_timeout(15000)
    page.goto("https://your-appian.example.com")

    InputUtils.setValueByLabelText(page, "Username", "demo_user")
    InputUtils.setValueByLabelText(page, "Password", "secret")
    ButtonUtils.clickByLabelText(page, "Sign In")

    browser.close()
```
