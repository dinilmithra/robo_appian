# DropdownUtils

The `DropdownUtils` class provides comprehensive methods for interacting with dropdown and combobox components in Appian applications. It handles the complex interactions required for Appian's dynamic dropdown elements, providing reliable selection and validation capabilities.

## Overview

DropdownUtils is designed to handle Appian's sophisticated dropdown structures, providing reliable methods to:

- Select dropdown values by visible label text
- Select values using partial label matching  
- Check if dropdown options exist
- Verify dropdown read-only status
- Handle combobox components directly
- Manage dynamic dropdown loading and selection

## Class Methods

### selectDropdownValueByLabelText()

Selects a value from a dropdown by its exact visible label text.


**Parameters:**
- `wait` (WebDriverWait): Selenium WebDriverWait instance for element waiting
- `dropdown_label` (str): The exact visible text label of the dropdown
- `value` (str): The value/option to select from the dropdown

**Usage Example:**
```python
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from robo_appian.components.DropdownUtils import DropdownUtils

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

# Select status from dropdown
DropdownUtils.selectDropdownValueByLabelText(wait, "Status", "Approved")

# Select department
DropdownUtils.selectDropdownValueByLabelText(wait, "Department", "Engineering")

# Select priority
DropdownUtils.selectDropdownValueByLabelText(wait, "Priority", "High")
```

---

### selectDropdownValueByPartialLabelText()

Selects a value from a dropdown using partial label text matching.


**Parameters:**
- `wait` (WebDriverWait): Selenium WebDriverWait instance for element waiting
- `dropdown_label` (str): Partial text that appears in the dropdown label
- `value` (str): The value/option to select from the dropdown

**Usage Example:**
```python
# If label is "Customer Status (Required)"
DropdownUtils.selectDropdownValueByPartialLabelText(wait, "Customer Status", "Active")

# If label is "Employee Department (Optional)"
DropdownUtils.selectDropdownValueByPartialLabelText(wait, "Department", "HR")
```

---

### checkDropdownOptionValueExists()

Checks if a specific value exists in a dropdown's options.


**Parameters:**
- `wait` (WebDriverWait): Selenium WebDriverWait instance for element waiting
- `dropdown_label` (str): The label of the dropdown to check
- `value` (str): The value to look for in the dropdown options

**Returns:**
- `bool`: True if the value exists, False otherwise

**Usage Example:**
```python
# Check if option exists before selecting
if DropdownUtils.checkDropdownOptionValueExists(wait, "Status", "Pending"):
    DropdownUtils.selectDropdownValueByLabelText(wait, "Status", "Pending")
    print("Status set to Pending")
else:
    print("Pending status not available")

# Conditional logic based on available options
available_statuses = ["Active", "Inactive", "Suspended"]
for status in available_statuses:
    if DropdownUtils.checkDropdownOptionValueExists(wait, "Status", status):
        DropdownUtils.selectDropdownValueByLabelText(wait, "Status", status)
        break
```

---

### checkReadOnlyStatusByLabelText()

Checks if a dropdown is in read-only mode.


**Parameters:**
- `wait` (WebDriverWait): Selenium WebDriverWait instance for element waiting
- `label` (str): The label of the dropdown to check

**Returns:**
- `bool`: True if the dropdown is read-only, False if it's editable

**Usage Example:**
```python
# Check if dropdown is editable before trying to select
if not DropdownUtils.checkReadOnlyStatusByLabelText(wait, "Status"):
    DropdownUtils.selectDropdownValueByLabelText(wait, "Status", "Approved")
else:
    print("Status dropdown is read-only")
```

---

### selectDropdownValueByComboboxComponent()

Selects a value from a dropdown using a direct combobox WebElement reference.


**Parameters:**
- `wait` (WebDriverWait): Selenium WebDriverWait instance for element waiting
- `combobox` (WebElement): The combobox WebElement to interact with
- `value` (str): The value to select from the dropdown

**Usage Example:**
```python
from selenium.webdriver.common.by import By

# Find combobox directly and select value
combobox = driver.find_element(By.ID, "combobox_id")
DropdownUtils.selectDropdownValueByComboboxComponent(wait, combobox, "Option Value")
```

## Best Practices

### Label-Based Selection

**Prefer exact label matching** for reliability:
```python
# ✅ Recommended - exact match
DropdownUtils.selectDropdownValueByLabelText(wait, "Employee Status", "Active")

# ⚠️ Use carefully - partial match
DropdownUtils.selectDropdownValueByPartialLabelText(wait, "Status", "Active")
```

### Validation Before Selection

**Check option availability** before selection:
```python
# Robust selection with validation
dropdown_label = "Priority"
desired_value = "High"

if DropdownUtils.checkDropdownOptionValueExists(wait, dropdown_label, desired_value):
    DropdownUtils.selectDropdownValueByLabelText(wait, dropdown_label, desired_value)
    print(f"Selected {desired_value}")
else:
    print(f"{desired_value} not available in {dropdown_label}")
```

### Handle Read-Only Dropdowns

**Verify dropdown state** before interaction:
```python
def safe_dropdown_selection(wait, label, value):
    if DropdownUtils.checkReadOnlyStatusByLabelText(wait, label):
        print(f"Dropdown '{label}' is read-only, skipping selection")
        return False
    
    if DropdownUtils.checkDropdownOptionValueExists(wait, label, value):
        DropdownUtils.selectDropdownValueByLabelText(wait, label, value)
        return True
    else:
        print(f"Value '{value}' not found in dropdown '{label}'")
        return False
```

### Error Handling

Always wrap dropdown interactions in try-catch blocks:
```python
try:
    DropdownUtils.selectDropdownValueByLabelText(wait, "Status", "Approved")
    print("Dropdown selection successful")
except Exception as e:
    print(f"Failed to select dropdown value: {e}")
```

## Common Use Cases

### Form Data Entry
```python
# Fill out application form
DropdownUtils.selectDropdownValueByLabelText(wait, "Country", "United States")
DropdownUtils.selectDropdownValueByLabelText(wait, "State", "California")
DropdownUtils.selectDropdownValueByLabelText(wait, "City", "San Francisco")
DropdownUtils.selectDropdownValueByLabelText(wait, "Employment Type", "Full-time")
```

### Filter and Search
```python
# Set search filters
DropdownUtils.selectDropdownValueByLabelText(wait, "Department", "Engineering")
DropdownUtils.selectDropdownValueByLabelText(wait, "Status", "Active")
DropdownUtils.selectDropdownValueByLabelText(wait, "Date Range", "Last 30 Days")
ButtonUtils.clickByLabelText(wait, "Apply Filters")
```

### Configuration Settings
```python
# Configure application settings
DropdownUtils.selectDropdownValueByLabelText(wait, "Time Zone", "Pacific Standard Time")
DropdownUtils.selectDropdownValueByLabelText(wait, "Language", "English")
DropdownUtils.selectDropdownValueByLabelText(wait, "Theme", "Dark Mode")
```

### Conditional Selections
```python
# Dynamic selection based on available options
priority_options = ["Critical", "High", "Medium", "Low"]
for priority in priority_options:
    if DropdownUtils.checkDropdownOptionValueExists(wait, "Priority", priority):
        DropdownUtils.selectDropdownValueByLabelText(wait, "Priority", priority)
        print(f"Priority set to: {priority}")
        break
```

## Technical Details

### Dropdown Interaction Flow

1. **Find Combobox**: Locate the dropdown combobox by label
2. **Click to Open**: Click the combobox to open dropdown options
3. **Get Options ID**: Extract the `aria-controls` attribute for option list ID
4. **Locate Option**: Find the specific option by value text
5. **Select Option**: Click the desired option

### XPath Strategies

**Exact Label Combobox:**
```xpath
.//div[./div/span[normalize-space(text())="{label}"]]/div/div/div/div[@role="combobox" and not(@aria-disabled="true")]
```

**Partial Label Combobox:**
```xpath
.//div[./div/span[contains(normalize-space(text()), "{label}")]]/div/div/div/div[@role="combobox" and not(@aria-disabled="true")]
```

**Option Selection:**
```xpath
.//div/ul[@id="{dropdown_option_id}"]/li[./div[normalize-space(text())="{value}"]]
```

### ARIA Attributes

DropdownUtils leverages ARIA attributes for reliable interaction:
- `role="combobox"` - Identifies dropdown components
- `aria-controls` - Links combobox to its option list
- `aria-disabled` - Checks if dropdown is disabled

## Troubleshooting

### Common Issues

**Dropdown Not Found:**
```
Exception: Could not find combobox with label "Status"
```
**Solutions:**
- Verify exact label text (check for punctuation, spaces)
- Ensure dropdown is visible and not inside collapsed sections
- Check if dropdown is dynamically loaded
- Use partial label matching if label has dynamic content

**Option Not Available:**
```
Exception: Could not find dropdown option "Approved" with dropdown option id "dropdown_123"
```
**Solutions:**
- Verify the exact option text
- Check if options are loaded dynamically
- Use `checkDropdownOptionValueExists()` to validate before selection
- Ensure dropdown is fully expanded before selection

**Dropdown is Read-Only:**
- Use `checkReadOnlyStatusByLabelText()` to verify state
- Check if user has permissions to modify the field
- Verify if dropdown becomes editable after other form interactions

### Debugging Tips

1. **Inspect Dropdown Structure**:
   ```html
   <div>
     <div><span>Status</span></div>
     <div role="combobox" aria-controls="options_123">
       <!-- Combobox content -->
     </div>
   </div>
   <ul id="options_123">
     <li><div>Active</div></li>
     <li><div>Inactive</div></li>
   </ul>
   ```

2. **Check Option Loading**:
   - Some dropdowns load options dynamically
   - Wait for options to be fully loaded before selection
   - Use explicit waits if needed

3. **Verify Dropdown State**:
   - Check if dropdown is enabled/disabled
   - Verify if dropdown is visible in current view
   - Ensure no overlays are blocking interaction

## Integration Examples

### With pytest and Parameterization
```python
import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from robo_appian.components.DropdownUtils import DropdownUtils

class TestDropdownSelections:
    def setup_method(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)
    
    def teardown_method(self):
        self.driver.quit()
    
    @pytest.mark.parametrize("dropdown,value", [
        ("Status", "Active"),
        ("Department", "Engineering"),
        ("Priority", "High"),
    ])
    def test_dropdown_selections(self, dropdown, value):
        self.driver.get("https://your-appian-app.com")
        
        # Validate option exists before selection
        assert DropdownUtils.checkDropdownOptionValueExists(
            self.wait, dropdown, value
        ), f"Option '{value}' not found in '{dropdown}' dropdown"
        
        # Select the value
        DropdownUtils.selectDropdownValueByLabelText(self.wait, dropdown, value)
```

### With Page Object Model
```python
class EmployeeFormPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def set_employee_details(self, department, status, employment_type):
        # Set department if dropdown is editable
        if not DropdownUtils.checkReadOnlyStatusByLabelText(self.wait, "Department"):
            DropdownUtils.selectDropdownValueByLabelText(self.wait, "Department", department)
        
        # Set status with validation
        if DropdownUtils.checkDropdownOptionValueExists(self.wait, "Status", status):
            DropdownUtils.selectDropdownValueByLabelText(self.wait, "Status", status)
        
        # Set employment type
        DropdownUtils.selectDropdownValueByLabelText(self.wait, "Employment Type", employment_type)
    
    def get_available_departments(self):
        # Custom method to extract all available options
        # Implementation would depend on specific requirements
        pass
```

### With Data-Driven Configuration
```python
import yaml
from robo_appian.components.DropdownUtils import DropdownUtils

# Load form configuration
with open('form_config.yaml') as f:
    config = yaml.safe_load(f)

# Fill dropdowns from configuration
for dropdown_config in config['dropdowns']:
    label = dropdown_config['label']
    value = dropdown_config['value']
    required = dropdown_config.get('required', False)
    
    if DropdownUtils.checkDropdownOptionValueExists(wait, label, value):
        DropdownUtils.selectDropdownValueByLabelText(wait, label, value)
    elif required:
        raise Exception(f"Required dropdown option '{value}' not found in '{label}'")
```

## Related Components

- **[InputUtils](input-utils.md)** - For text input field interactions
- **[ButtonUtils](button-utils.md)** - For form submission after dropdown selection
- **[SearchDropdownUtils](search-dropdown-utils.md)** - For searchable dropdown components
- **[ComponentDriver](component-driver.md)** - For universal component interactions

---

*DropdownUtils provides robust dropdown interaction capabilities for Appian applications, handling the complexity of dynamic option loading and selection while maintaining reliability and ease of use.*
