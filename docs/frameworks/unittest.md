# Using Robo Appian with Unittest

This page explains how to use Robo Appian in your Unittest-based test suites.

## Installation

Make sure you have `selenium` and `robo_appian` installed:

```bash
pip install selenium robo_appian
```

## Example: Basic Unittest Test

```python
import unittest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from robo_appian.components.InputUtils import InputUtils
from robo_appian.components.ButtonUtils import ButtonUtils

class TestLogin(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        self.driver.quit()

    def test_login(self):
        self.driver.get("https://your-appian-app.com")
        InputUtils.setValueByLabelText(self.wait, "Username", "test_user")
        InputUtils.setValueByLabelText(self.wait, "Password", "password123")
        ButtonUtils.clickByLabelText(self.wait, "Sign In")
        # Add assertions here

if __name__ == "__main__":
    unittest.main()
```

## Tips
- Use `setUp` and `tearDown` for WebDriver lifecycle
- Use assertions to validate outcomes
- Integrate with CI/CD for automated test runs
