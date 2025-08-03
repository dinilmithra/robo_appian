# ButtonUtils

The `ButtonUtils` class provides convenient methods for interacting with button components in Appian applications. It simplifies button interactions by allowing you to locate and click buttons using their visible labels or HTML attributes.

## Overview

ButtonUtils is designed to handle Appian's dynamic button structures, providing reliable methods to:

- Click buttons by their visible label text
- Click buttons by their HTML ID
- Handle Appian's complex button hierarchies automatically

## Class Methods

### clickByLabelText()

Finds a button by its visible label text and clicks it.


**Parameters:**
- `wait` (WebDriverWait): Selenium WebDriverWait instance for element waiting
- `label` (str): The visible text label of the button to click

**Usage Example:**
```python
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from robo_appian.components.ButtonUtils import ButtonUtils

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

# Click a submit button
ButtonUtils.clickByLabelText(wait, "Submit")

# Click a cancel button
ButtonUtils.clickByLabelText(wait, "Cancel")

# Click a save button
ButtonUtils.clickByLabelText(wait, "Save Changes")
```

**Error Handling:**
Raises `RuntimeError` if the button is not found or not clickable.

---

### clickById()

Finds a button by its HTML ID attribute and clicks it.

**Signature:**
```python
@staticmethod
def clickById(wait: WebDriverWait, id: str) -> None
```

**Parameters:**
- `wait` (WebDriverWait): Selenium WebDriverWait instance for element waiting
- `id` (str): The HTML ID attribute of the button to click

**Usage Example:**
```python
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from robo_appian.components.ButtonUtils import ButtonUtils

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

# Click a button by its ID
ButtonUtils.clickById(wait, "submit_button_id")

# Click another button by ID
ButtonUtils.clickById(wait, "cancel_btn")
```

**Error Handling:**
Raises `RuntimeError` if the button with the specified ID is not found or not clickable.

## Best Practices

### Label-Based vs ID-Based Selection

**Prefer label-based selection** when possible:
```python
# ✅ Recommended - more readable and maintainable
ButtonUtils.clickByLabelText(wait, "Submit Application")

# ❌ Less preferred - brittle and hard to understand
ButtonUtils.clickById(wait, "btn_submit_app_v2_final")
```

### Handle Dynamic Labels

For buttons with dynamic or partial labels, ensure you use the exact text:
```python
# If button shows "Submit (3 items)"
ButtonUtils.clickByLabelText(wait, "Submit (3 items)")

# For partial matching, consider using contains in custom XPath
```

### Error Handling

Always wrap button interactions in try-catch blocks for robust error handling:
```python
try:
    ButtonUtils.clickByLabelText(wait, "Submit")
    print("Button clicked successfully")
except RuntimeError as e:
    print(f"Failed to click button: {e}")
```

## Common Use Cases

### Form Submission
```python
# Fill form and submit
InputUtils.setValueByLabelText(wait, "Name", "John Doe")
InputUtils.setValueByLabelText(wait, "Email", "john@example.com")
ButtonUtils.clickByLabelText(wait, "Submit")
```

### Navigation
```python
# Navigate through application
ButtonUtils.clickByLabelText(wait, "Next")
ButtonUtils.clickByLabelText(wait, "Previous")
ButtonUtils.clickByLabelText(wait, "Finish")
```

### Dialog Actions
```python
# Handle confirmation dialogs
ButtonUtils.clickByLabelText(wait, "Confirm")
ButtonUtils.clickByLabelText(wait, "Cancel")
ButtonUtils.clickByLabelText(wait, "OK")
```

### File Operations
```python
# File upload/download actions
ButtonUtils.clickByLabelText(wait, "Upload File")
ButtonUtils.clickByLabelText(wait, "Download")
ButtonUtils.clickByLabelText(wait, "Browse")
```

## Technical Details

### XPath Strategy

ButtonUtils uses sophisticated XPath expressions to locate buttons:
```xpath
.//button[./span[contains(translate(normalize-space(.), '\u00a0', ' '), '{label}')]]
```

This XPath:
- Looks for `<button>` elements
- Searches for nested `<span>` elements containing the label text
- Handles non-breaking spaces and whitespace normalization
- Uses case-sensitive matching for precision

### Element Wait Strategy

- Uses `EC.element_to_be_clickable()` to ensure buttons are ready for interaction
- Respects the WebDriverWait timeout settings
- Automatically handles Appian's dynamic loading states

## Troubleshooting

### Common Issues

**Button Not Found:**
```
RuntimeError: Button with label 'Submit' not found or not clickable.
```
**Solutions:**
- Verify the exact button text (check for extra spaces, special characters)
- Ensure the button is visible and not disabled
- Wait for any loading states to complete
- Check if button is inside a frame or dialog

**Button Not Clickable:**
```
RuntimeError: Button with label 'Submit' not found or not clickable.
```
**Solutions:**
- Increase WebDriverWait timeout
- Ensure no overlays or modals are blocking the button
- Verify button is not disabled in the UI
- Check if page is fully loaded

### Debugging Tips

1. **Inspect the button element** in browser developer tools
2. **Verify the exact text content** including hidden characters
3. **Check button state** (enabled/disabled, visible/hidden)
4. **Use explicit waits** before button interactions

## Integration Examples

### With pytest
```python
import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from robo_appian.components.ButtonUtils import ButtonUtils

class TestButtonInteractions:
    def setup_method(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)
    
    def teardown_method(self):
        self.driver.quit()
    
    def test_submit_button_click(self):
        self.driver.get("https://your-appian-app.com")
        ButtonUtils.clickByLabelText(self.wait, "Submit")
        # Add assertions here
```

### With Page Object Model
```python
class AppianFormPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def submit_form(self):
        ButtonUtils.clickByLabelText(self.wait, "Submit")
    
    def cancel_form(self):
        ButtonUtils.clickByLabelText(self.wait, "Cancel")
```

## Related Components

- **[InputUtils](input-utils.md)** - For form field interactions
- **[DropdownUtils](dropdown-utils.md)** - For dropdown selections
- **[LinkUtils](link-utils.md)** - For link navigation
- **[ComponentDriver](component-driver.md)** - For universal component interactions

---

*ButtonUtils provides the foundation for reliable button interactions in Appian applications, abstracting away the complexity of Appian's dynamic UI structure.*
