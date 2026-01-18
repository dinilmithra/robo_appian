# pytest Integration

Use fixtures to share the browser and `WebDriverWait` across tests.

## Sample `conftest.py`
```python
import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

@pytest.fixture(scope="session")
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

@pytest.fixture
def wait(driver):
    return WebDriverWait(driver, 10)
```

## Example test
```python
from robo_appian.components import InputUtils, ButtonUtils


def test_login(wait):
    driver = wait._driver
    driver.get("https://your-appian.example.com")

    InputUtils.setValueByLabelText(wait, "Username", "demo_user")
    InputUtils.setValueByLabelText(wait, "Password", "SuperSecret!")
    ButtonUtils.clickByLabelText(wait, "Sign In")
```

## Tips
- Keep fixtures small; prefer one `wait` fixture that wraps a shared driver.
- If tests need isolation, change driver fixture scope to `function`.
- Add markers for slow/UI tests and run with `pytest -m ui` in CI.
