# Quick Start

Automate a simple Appian login page with label-driven selectors.

## Minimal example
```python
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from robo_appian.components import InputUtils, ButtonUtils

# Launch browser
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

# Navigate to your Appian site
driver.get("https://your-appian.example.com")

# Interact by label
InputUtils.setValueByLabelText(wait, "Username", "demo_user")
InputUtils.setValueByLabelText(wait, "Password", "SuperSecret!")
ButtonUtils.clickByLabelText(wait, "Sign In")
```

Key points:
- Pass `wait` first. Utilities derive `driver` from `wait._driver` internally.
- Inputs and buttons are located by visible labels; NBSPs and whitespace are normalized.
- `ComponentUtils.click` wraps ActionChains and clickability waits to handle overlays/animations.

## Next steps
- Explore component patterns: [Components guide](../user-guide/components.md)
- See working flows: [Examples](../examples/login.md)
- Browse APIs: [API Reference](../api/index.md)
