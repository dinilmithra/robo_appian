# InputUtils

The `InputUtils` class provides comprehensive methods for interacting with input components in Appian applications. It handles text fields, text areas, and other input elements, making it easy to set values using visible labels or HTML attributes.

## Overview

InputUtils is designed to handle Appian's complex input field structures, providing reliable methods to:

- Set values in input fields by their visible label text
- Set values using partial label matching
- Set values by HTML ID
- Handle various input types (text, password, email, etc.)
- Manage Appian's dynamic form components

## Class Methods

### setValueByLabelText()

Sets a value in an input component by its exact visible label text.

**Signature:**
```python
@staticmethod
def setValueByLabelText(wait: WebDriverWait, label: str, value: str) -> None
```

**Parameters:**
- `wait` (WebDriverWait): Selenium WebDriverWait instance for element waiting
- `label` (str): The exact visible text label of the input component
- `value` (str): The value to set in the input field

**Usage Example:**
```python
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from robo_appian.components.InputUtils import InputUtils

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

# Set username
InputUtils.setValueByLabelText(wait, "Username", "john_doe")

# Set email
InputUtils.setValueByLabelText(wait, "Email Address", "john@example.com")

# Set password
InputUtils.setValueByLabelText(wait, "Password", "secure_password123")
```

---

### setValueByPartialLabelText()

Sets a value in an input component using partial label text matching.

**Signature:**
```python
@staticmethod
def setValueByPartialLabelText(wait: WebDriverWait, label: str, value: str) -> None
```

**Parameters:**
- `wait` (WebDriverWait): Selenium WebDriverWait instance for element waiting
- `label` (str): Partial text that appears in the label of the input component
- `value` (str): The value to set in the input field

**Usage Example:**
```python
# If label is "Customer Name (Required)"
InputUtils.setValueByPartialLabelText(wait, "Customer Name", "John Smith")

# If label is "Phone Number (Optional)"
InputUtils.setValueByPartialLabelText(wait, "Phone", "+1-555-123-4567")
```

**Note:** Use partial matching carefully to avoid ambiguous matches.

---

### setValueById()

Sets a value in an input component by its HTML ID attribute.

**Signature:**
```python
@staticmethod
def setValueById(wait: WebDriverWait, component_id: str, value: str) -> WebElement
```

**Parameters:**
- `wait` (WebDriverWait): Selenium WebDriverWait instance for element waiting
- `component_id` (str): The HTML ID attribute of the input component
- `value` (str): The value to set in the input field

**Returns:**
- `WebElement`: The input component after setting the value

**Usage Example:**
```python
# Set value by ID
component = InputUtils.setValueById(wait, "username_input", "john_doe")

# Chain operations if needed
InputUtils.setValueById(wait, "email_field", "john@example.com")
```

## Best Practices

### Label-Based vs ID-Based Selection

**Prefer label-based selection** for maintainability:
```python
# ✅ Recommended - readable and maintainable
InputUtils.setValueByLabelText(wait, "Customer Name", "John Smith")

# ❌ Less preferred - brittle and technical
InputUtils.setValueById(wait, "cust_nm_fld_v2", "John Smith")
```

### Handle Special Characters

Appian input fields can handle various data types:
```python
# Text with special characters
InputUtils.setValueByLabelText(wait, "Description", "Special chars: @#$%^&*()")

# Numeric values (as strings)
InputUtils.setValueByLabelText(wait, "Amount", "1234.56")

# Dates (format depends on field configuration)
InputUtils.setValueByLabelText(wait, "Start Date", "01/15/2024")
```

### Clear and Set Pattern

InputUtils automatically clears fields before setting new values:
```python
# This will clear existing content and set new value
InputUtils.setValueByLabelText(wait, "Notes", "New content")
```

### Error Handling

Always handle potential exceptions:
```python
try:
    InputUtils.setValueByLabelText(wait, "Username", "john_doe")
    print("Value set successfully")
except Exception as e:
    print(f"Failed to set input value: {e}")
```

## Common Use Cases

### User Registration Form
```python
# Fill out registration form
InputUtils.setValueByLabelText(wait, "First Name", "John")
InputUtils.setValueByLabelText(wait, "Last Name", "Doe")
InputUtils.setValueByLabelText(wait, "Email", "john.doe@example.com")
InputUtils.setValueByLabelText(wait, "Phone", "+1-555-123-4567")
InputUtils.setValueByLabelText(wait, "Password", "SecurePass123!")
InputUtils.setValueByLabelText(wait, "Confirm Password", "SecurePass123!")
```

### Search Forms
```python
# Search functionality
InputUtils.setValueByLabelText(wait, "Search Terms", "quarterly report")
InputUtils.setValueByPartialLabelText(wait, "Category", "Finance")
ButtonUtils.clickByLabelText(wait, "Search")
```

### Data Entry Forms
```python
# Employee information
InputUtils.setValueByLabelText(wait, "Employee ID", "EMP001")
InputUtils.setValueByLabelText(wait, "Department", "Engineering")
InputUtils.setValueByLabelText(wait, "Start Date", "01/15/2024")
InputUtils.setValueByLabelText(wait, "Salary", "75000")
```

### Profile Updates
```python
# Update user profile
InputUtils.setValueByLabelText(wait, "Bio", "Software engineer with 5+ years experience")
InputUtils.setValueByLabelText(wait, "Skills", "Python, Selenium, Test Automation")
InputUtils.setValueByLabelText(wait, "Location", "San Francisco, CA")
```

## Technical Details

### Label-to-Input Mapping

InputUtils uses sophisticated logic to map labels to inputs:

1. **Find Label Elements**: Locates `<label>` elements by text
2. **Extract `for` Attribute**: Gets the target input ID from label's `for` attribute
3. **Locate Input Element**: Finds the input element by the extracted ID
4. **Ensure Clickable**: Waits for the input to be in a clickable state

### XPath Strategies

**Exact Label Match:**
```xpath
.//div/label[normalize-space(text())="{label}"]
```

**Partial Label Match:**
```xpath
.//div/label[contains(normalize-space(text()), "{label}")]
```

### Input Value Setting

The `_setValueByComponent()` method:
1. **Clears** existing content using `clear()`
2. **Sets** new value using `send_keys()`
3. **Handles** various input types automatically

## Troubleshooting

### Common Issues

**Input Field Not Found:**
```
Exception: Could not find clickable input component with id 'field_id'
```
**Solutions:**
- Verify the exact label text (check spacing and punctuation)
- Ensure the input field is visible and enabled
- Check if the input is inside a collapsed section or tab
- Wait for any dynamic loading to complete

**Label Missing `for` Attribute:**
```
ValueError: Input component with label 'Field Name' does not have 'for' attribute
```
**Solutions:**
- Use `setValueById()` if you know the input ID
- Inspect the HTML to understand the label-input relationship
- Contact developers to ensure proper label associations

### Debugging Tips

1. **Inspect Label-Input Association**:
   ```html
   <label for="input_123">Username</label>
   <input id="input_123" type="text" />
   ```

2. **Check Input State**:
   - Verify input is visible and enabled
   - Ensure no validation errors prevent input
   - Check if input accepts the data type you're providing

3. **Verify Exact Label Text**:
   ```python
   # Check for exact match - these are different:
   "Username"
   "Username:"
   "Username (Required)"
   " Username "  # Leading/trailing spaces
   ```

## Integration Examples

### With pytest and Data-Driven Tests
```python
import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from robo_appian.components.InputUtils import InputUtils

class TestFormInputs:
    def setup_method(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)
    
    def teardown_method(self):
        self.driver.quit()
    
    @pytest.mark.parametrize("field,value", [
        ("Username", "testuser"),
        ("Email", "test@example.com"),
        ("Phone", "555-1234"),
    ])
    def test_input_fields(self, field, value):
        self.driver.get("https://your-appian-app.com")
        InputUtils.setValueByLabelText(self.wait, field, value)
        # Add verification logic
```

### With Page Object Model
```python
class UserProfilePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def update_basic_info(self, first_name, last_name, email):
        InputUtils.setValueByLabelText(self.wait, "First Name", first_name)
        InputUtils.setValueByLabelText(self.wait, "Last Name", last_name)
        InputUtils.setValueByLabelText(self.wait, "Email", email)
    
    def set_contact_info(self, phone, address):
        InputUtils.setValueByLabelText(self.wait, "Phone", phone)
        InputUtils.setValueByLabelText(self.wait, "Address", address)
```

### With Configuration-Driven Tests
```python
import json
from robo_appian.components.InputUtils import InputUtils

# Load test data from JSON
with open('test_data.json') as f:
    test_data = json.load(f)

# Fill form from configuration
for field_name, field_value in test_data['form_fields'].items():
    InputUtils.setValueByLabelText(wait, field_name, field_value)
```

## Related Components

- **[ButtonUtils](button-utils.md)** - For button interactions after input
- **[DropdownUtils](dropdown-utils.md)** - For dropdown field selections
- **[DateUtils](date-utils.md)** - For specialized date input handling
- **[ComponentDriver](component-driver.md)** - For universal component interactions

---

*InputUtils provides the foundation for reliable form interactions in Appian applications, handling the complexity of dynamic form structures while maintaining simple, readable test code.*
