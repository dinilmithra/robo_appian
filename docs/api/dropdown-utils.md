# Dropdown Utils

## Overview

DropdownUtils provides methods to interact with Appian dropdown components. Use DropdownUtils to select options from dropdowns by their label, check if dropdowns are enabled or read-only, retrieve all available options, and verify specific options exist. Dropdowns use the combobox ARIA pattern with clickable triggers and option lists.

## Methods

### selectDropdownValueByLabelText

Select an option from a dropdown by the dropdown's exact label text.

Use this when you need to select a specific option from a dropdown and you know the exact label text displayed next to or above the dropdown. This method clicks the dropdown to open it, waits for options to appear, then clicks the desired option. Perfect for form submissions where dropdown selections are required.

**Args:**

- `wait` (WebDriverWait): WebDriverWait instance with configured timeout
- `label` (str): Exact label text for the dropdown
- `value` (str): Exact text of the option to select from the dropdown

**Raises:**

- `TimeoutException`: If dropdown or option not found or not clickable within timeout

**Returns:** None

**Examples:**

HTML:
```html
<div role="presentation">
  <span>Status</span>
  <div role="combobox" aria-controls="dropdown_123_list">
    <span>Select...</span>
  </div>
</div>
<!-- After clicking combobox -->
<ul id="dropdown_123_list" role="listbox">
  <li role="option"><div>Active</div></li>
  <li role="option"><div>Inactive</div></li>
</ul>
```

Python:
```python
from robo_appian.components.DropdownUtils import DropdownUtils
from selenium.webdriver.support.ui import WebDriverWait

DropdownUtils.selectDropdownValueByLabelText(wait, "Status", "Active")
```

---

### selectDropdownValueByPartialLabelText

Select an option from a dropdown using partial label text matching.

Use this when the dropdown label contains dynamic text or you only know part of the label. This method uses a contains match instead of exact match, making it useful for labels with counters, dates, or other variable content appended.

**Args:**

- `wait` (WebDriverWait): WebDriverWait instance with configured timeout
- `label` (str): Partial label text for the dropdown (uses contains matching)
- `value` (str): Exact text of the option to select

**Raises:**

- `TimeoutException`: If dropdown or option not found within timeout

**Returns:** None

**Examples:**

HTML:
```html
<div role="presentation">
  <span>Department (25 items)</span>
  <div role="combobox" aria-controls="dropdown_456_list">
    <span>Select...</span>
  </div>
</div>
```

Python:
```python
from robo_appian.components.DropdownUtils import DropdownUtils
from selenium.webdriver.support.ui import WebDriverWait

DropdownUtils.selectDropdownValueByPartialLabelText(wait, "Department", "Sales")
```

---

### checkEditableStatusByLabelText

Check if a dropdown is enabled (editable) or disabled by its label.

Use this to verify whether a dropdown is interactive before attempting to select options. Returns True if the dropdown is editable, False if it's disabled. Useful in test assertions to verify conditional dropdown states based on other form selections.

**Args:**

- `wait` (WebDriverWait): WebDriverWait instance with configured timeout
- `label` (str): Exact label text for the dropdown

**Raises:** None (returns False if dropdown not found)

**Returns:** bool: True if dropdown is editable, False if disabled or not found

**Examples:**

HTML:
```html
<!-- Enabled dropdown -->
<div role="presentation">
  <span>Region</span>
  <div role="combobox" aria-disabled="false">Select...</div>
</div>

<!-- Disabled dropdown -->
<div role="presentation">
  <span>Restricted Field</span>
  <div aria-disabled="true">Not Available</div>
</div>
```

Python:
```python
from robo_appian.components.DropdownUtils import DropdownUtils
from selenium.webdriver.support.ui import WebDriverWait

if DropdownUtils.checkEditableStatusByLabelText(wait, "Region"):
    DropdownUtils.selectDropdownValueByLabelText(wait, "Region", "North")
```

---

### getDropdownOptionValues

Retrieve all available option values from a dropdown as a list.

Use this when you need to verify all available options, validate dropdown content, or make dynamic selections based on available choices. This method opens the dropdown, extracts all option texts, closes the dropdown, and returns the list of options.

**Args:**

- `wait` (WebDriverWait): WebDriverWait instance with configured timeout
- `label` (str): Exact label text for the dropdown

**Raises:**

- `TimeoutException`: If dropdown not found within timeout

**Returns:** list[str]: List of all option texts in the dropdown

**Examples:**

HTML:
```html
<div role="presentation">
  <span>Priority</span>
  <div role="combobox" aria-controls="dropdown_789_list">Select...</div>
</div>
<ul id="dropdown_789_list" role="listbox">
  <li role="option"><div>High</div></li>
  <li role="option"><div>Medium</div></li>
  <li role="option"><div>Low</div></li>
</ul>
```

Python:
```python
from robo_appian.components.DropdownUtils import DropdownUtils
from selenium.webdriver.support.ui import WebDriverWait

options = DropdownUtils.getDropdownOptionValues(wait, "Priority")
print(options)  # ['High', 'Medium', 'Low']
assert "High" in options, "High priority option missing"
```

---

### checkReadOnlyStatusByLabelText

Check if a dropdown is read-only (disabled) by its label.

Use this to verify whether a dropdown is in read-only mode, typically displaying a static value without allowing interaction. This is the inverse of checkEditableStatusByLabelText. Returns True if the dropdown is read-only, False if it's editable or interactive.

**Args:**

- `wait` (WebDriverWait): WebDriverWait instance with configured timeout
- `label` (str): Exact label text for the dropdown

**Raises:** None (returns False if dropdown not found or an error occurs)

**Returns:** bool: True if dropdown is read-only, False if editable or not found

**Examples:**

HTML:
```html
<!-- Read-only dropdown -->
<div role="presentation">
  <span>Approval Status</span>
  <div aria-labelledby="status_label">Approved</div>
</div>

<!-- Editable dropdown -->
<div role="presentation">
  <span>Department</span>
  <div role="combobox">Select...</div>
</div>
```

Python:
```python
from robo_appian.components.DropdownUtils import DropdownUtils
from selenium.webdriver.support.ui import WebDriverWait

if DropdownUtils.checkReadOnlyStatusByLabelText(wait, "Approval Status"):
    print("Dropdown is read-only, cannot modify")
else:
    DropdownUtils.selectDropdownValueByLabelText(wait, "Approval Status", "Pending")
```

---

### selectDropdownValueByComboboxComponent

Select a dropdown option when you already have the combobox WebElement.

Use this advanced method when you've already located the combobox element through other means and want to select an option directly. Useful in complex scenarios where you're iterating through multiple dropdowns or have custom element discovery logic. Skips the label-based lookup step.

**Args:**

- `wait` (WebDriverWait): WebDriverWait instance with configured timeout
- `combobox` (WebElement): The combobox WebElement already located
- `value` (str): Exact text of the option to select

**Raises:**

- `TimeoutException`: If option not found within timeout
- `ValueError`: If combobox lacks required attributes

**Returns:** None

**Examples:**

HTML:
```html
<div role="combobox" id="custom_dropdown" aria-controls="options_list">
  <span>Select...</span>
</div>
<ul id="options_list" role="listbox">
  <li role="option"><div>Option A</div></li>
  <li role="option"><div>Option B</div></li>
</ul>
```

Python:
```python
from robo_appian.components.DropdownUtils import DropdownUtils
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

combobox = wait.until(EC.element_to_be_clickable((By.ID, "custom_dropdown")))
DropdownUtils.selectDropdownValueByComboboxComponent(wait, combobox, "Option A")
```

---

### waitForDropdownToBeEnabled

Wait for a dropdown to transition from disabled to enabled state.

Use this when a dropdown becomes interactive after other form actions complete (e.g., after selecting a region, the city dropdown becomes enabled). Polls the dropdown's editable status at regular intervals until it becomes enabled or the timeout expires. Useful for handling dynamic form behavior.

**Args:**

- `wait` (WebDriverWait): WebDriverWait instance with configured timeout
- `label` (str): Exact label text for the dropdown
- `wait_interval` (float): Seconds to wait between status checks (default: 0.5)
- `timeout` (int): Maximum seconds to wait for dropdown to enable (default: 2)

**Raises:** None (returns False if timeout expires)

**Returns:** bool: True if dropdown becomes enabled within timeout, False otherwise

**Examples:**

HTML:
```html
<div role="presentation">
  <span>Country</span>
  <div role="combobox">Select...</div>
</div>
<!-- Initially disabled -->
<div role="presentation">
  <span>State</span>
  <div aria-disabled="true">Select country first</div>
</div>
<!-- After selecting country, becomes enabled -->
```

Python:
```python
from robo_appian.components.DropdownUtils import DropdownUtils
from selenium.webdriver.support.ui import WebDriverWait

DropdownUtils.selectDropdownValueByLabelText(wait, "Country", "United States")

if DropdownUtils.waitForDropdownToBeEnabled(wait, "State", wait_interval=0.5, timeout=5):
    DropdownUtils.selectDropdownValueByLabelText(wait, "State", "California")
else:
    print("State dropdown did not become enabled")
```

---

### checkDropdownOptionValueExists

Check if a specific option value exists in a dropdown's option list.

Use this to verify that expected options are available before attempting to select them, or to validate dropdown content in tests. Opens the dropdown, searches for the option, and returns whether it exists. Non-destructive check that doesn't modify the dropdown selection.

**Args:**

- `wait` (WebDriverWait): WebDriverWait instance with configured timeout
- `label` (str): Exact label text for the dropdown
- `value` (str): Exact text of the option to check for

**Raises:**

- `TimeoutException`: If dropdown not found within timeout

**Returns:** bool: True if the option exists in the dropdown, False otherwise

**Examples:**

HTML:
```html
<div role="presentation">
  <span>Priority</span>
  <div role="combobox" aria-controls="priority_list">Select...</div>
</div>
<ul id="priority_list" role="listbox">
  <li role="option"><div>High</div></li>
  <li role="option"><div>Medium</div></li>
</ul>
```

Python:
```python
from robo_appian.components.DropdownUtils import DropdownUtils
from selenium.webdriver.support.ui import WebDriverWait

if DropdownUtils.checkDropdownOptionValueExists(wait, "Priority", "High"):
    DropdownUtils.selectDropdownValueByLabelText(wait, "Priority", "High")
else:
    print("High priority option not available")

assert DropdownUtils.checkDropdownOptionValueExists(wait, "Priority", "Critical"), "Critical option missing"
```

---

### waitForDropdownValuesToBeChanged

Wait for a dropdown's available options to change from an initial set of values.

Use this when dropdown options are dynamically populated based on other form selections. Compares the current dropdown options against an initial snapshot, polling at regular intervals until the options change or timeout expires. Essential for handling cascading dropdowns where options in one dropdown depend on the selection in another.

**Args:**

- `wait` (WebDriverWait): WebDriverWait instance with configured timeout
- `label` (str): Exact label text for the dropdown
- `initial_values` (list[str]): Initial list of option values to compare against
- `poll_frequency` (float): Seconds to wait between checks (default: 0.5)
- `timeout` (int): Maximum seconds to wait for values to change (default: 2)

**Raises:**

- `TimeoutException`: If dropdown not found within timeout

**Returns:** None (exits loop when values change or timeout expires)

**Examples:**

HTML:
```html
<div role="presentation">
  <span>Department</span>
  <div role="combobox">Select...</div>
</div>
<!-- Job Title dropdown options change based on Department selection -->
<div role="presentation">
  <span>Job Title</span>
  <div role="combobox" aria-controls="job_list">Select...</div>
</div>
```

Python:
```python
from robo_appian.components.DropdownUtils import DropdownUtils
from selenium.webdriver.support.ui import WebDriverWait

initial_jobs = DropdownUtils.getDropdownOptionValues(wait, "Job Title")
DropdownUtils.selectDropdownValueByLabelText(wait, "Department", "Engineering")

DropdownUtils.waitForDropdownValuesToBeChanged(
    wait, 
    "Job Title", 
    initial_jobs, 
    poll_frequency=0.5, 
    timeout=5
)

new_jobs = DropdownUtils.getDropdownOptionValues(wait, "Job Title")
print(f"Job titles updated: {new_jobs}")
```