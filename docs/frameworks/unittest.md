# unittest Integration

Use `setUp`/`tearDown` to manage the browser and `WebDriverWait`.

```python
import unittest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from robo_appian.components import InputUtils, ButtonUtils

class LoginTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        self.driver.quit()

    def test_login(self):
        self.driver.get("https://your-appian.example.com")
        InputUtils.setValueByLabelText(self.wait, "Username", "demo_user")
        InputUtils.setValueByLabelText(self.wait, "Password", "SuperSecret!")
        ButtonUtils.clickByLabelText(self.wait, "Sign In")

if __name__ == "__main__":
    unittest.main()
```

Adjust the timeout or add helpers like `RoboUtils.retry_on_timeout` inside tests if certain steps are flaky.
