# unittest Integration

Use Playwright setup and teardown hooks, then pass `page` to robo_appian utilities.

## Example
```python
import unittest
from playwright.sync_api import sync_playwright
from robo_appian import ButtonUtils, InputUtils

class LoginTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch()

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.playwright.stop()

    def setUp(self):
        self.context = self.browser.new_context()
        self.page = self.context.new_page()
        self.page.set_default_timeout(15000)

    def tearDown(self):
        self.context.close()

    def test_login(self):
        self.page.goto("https://your-appian.example.com")
        InputUtils.setValueByLabelText(self.page, "Username", "demo")
        ButtonUtils.clickByLabelText(self.page, "Sign In")
```
