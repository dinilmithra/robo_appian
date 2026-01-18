# Login Flow

A simple login automation using label-based selectors.

## Basic Login

```python
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from robo_appian.components import InputUtils, ButtonUtils

APP_URL = "https://your-appian.example.com"

with webdriver.Chrome() as driver:
    wait = WebDriverWait(driver, 10)
    driver.get(APP_URL)

    InputUtils.setValueByLabelText(wait, "Username", "demo_user")
    InputUtils.setValueByLabelText(wait, "Password", "SuperSecret!")
    ButtonUtils.clickByLabelText(wait, "Sign In")
```

## Login with SSO/Identity Provider

```python
from robo_appian.components import ButtonUtils, InputUtils
from selenium.webdriver.support.ui import WebDriverWait

# Click SSO identity provider button
ButtonUtils.clickByLabelText(wait, "Sign in with Azure AD")

# Wait for redirect to identity provider
InputUtils.setValueByLabelText(wait, "Email", "user@company.com")
ButtonUtils.clickByLabelText(wait, "Next")

# Enter password on IDP page
InputUtils.setValueByLabelText(wait, "Password", "SecurePassword123!")
ButtonUtils.clickByLabelText(wait, "Sign in")
```

## Login with Dynamic Labels

When labels include dynamic text like environment names:

```python
from robo_appian.components import InputUtils, ButtonUtils

# Use partial label matching for dynamic labels
InputUtils.setValueByPartialLabelText(wait, "Username", "demo_user")
InputUtils.setValueByPartialLabelText(wait, "Password", "SuperSecret!")
ButtonUtils.clickByPartialLabelText(wait, "Sign In")
```

## Verify Successful Login

```python
from robo_appian.components import LabelUtils

# Verify user logged in by checking for welcome message
LabelUtils.isLabelExists(wait, "Welcome, John Doe")

# Or verify a dashboard element is present
LabelUtils.isLabelExists(wait, "My Tasks")
```

Tips:
- Use exact labels when stable; switch to partial label methods if the UI appends text (e.g., "Username (prod)").
- For SSO/IDP flows, wait for visibility of the identity provider button and click via `ButtonUtils.clickByLabelText`.
- Add explicit waits after login to ensure the next page loads before continuing.
