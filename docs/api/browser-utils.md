# Browser Utils

## Overview

BrowserUtils provides tab and window management for multi-tab browser workflows. Switch between tabs, navigate to new tabs, and close tabs programmatically.

Use these utilities when your Appian automation requires opening links in new tabs, managing multiple browser windows, or handling popup windows.

## Methods

### switch_to_Tab

Switch to a specific browser tab by its index.

Use this when you know which tab you need (e.g., after opening a link in a new tab). Tab indices are zero-based: 0 is the first tab, 1 is the second, etc.

**Args:**

- `wait` (WebDriverWait): WebDriverWait instance
- `tab_number` (int): Zero-based index of the tab to switch to

**Returns:**

- None

**Raises:**

- `IndexError`: If tab_number is out of range for available tabs

**Examples:**

HTML:
```html
<!-- Link that opens in new tab -->
<a href="/report" target="_blank">View Report</a>
```

Python:
```python
from robo_appian.utils.BrowserUtils import BrowserUtils
from robo_appian.components.LinkUtils import LinkUtils

# Click link that opens new tab
LinkUtils.click(wait, "View Report")

# Switch to the new tab (second tab = index 1)
BrowserUtils.switch_to_Tab(wait, 1)

# Now interact with content in the new tab
# ...

# Switch back to first tab
BrowserUtils.switch_to_Tab(wait, 0)
```

---

### switch_to_next_tab

Switch to the next browser tab in sequence.

Use this to cycle through tabs when you don't know the exact index. If already on the last tab, wraps around to the first tab.

**Args:**

- `wait` (WebDriverWait): WebDriverWait instance

**Returns:**

- None

**Examples:**

Python:
```python
from robo_appian.utils.BrowserUtils import BrowserUtils

# Cycle through all open tabs
BrowserUtils.switch_to_next_tab(wait)  # Move to next tab
BrowserUtils.switch_to_next_tab(wait)  # Move to next tab again

# Process content in each tab
```

**Example - Processing Multiple Report Tabs:**

```python
from robo_appian.utils.BrowserUtils import BrowserUtils
from robo_appian.components.LinkUtils import LinkUtils
from selenium.webdriver.support.ui import WebDriverWait

# Open multiple reports in new tabs
LinkUtils.click(wait, "Sales Report")
LinkUtils.click(wait, "Inventory Report")
LinkUtils.click(wait, "Finance Report")

# Get initial tab count
initial_tabs = len(wait._driver.window_handles)

# Process each report tab
for _ in range(initial_tabs):
    # Do something in current tab
    print(f"Processing: {wait._driver.title}")
    
    # Move to next tab
    BrowserUtils.switch_to_next_tab(wait)
```

---

### close_current_tab_and_switch_back

Close the current browser tab and return to the previous tab.

Use this after completing work in a new tab and wanting to return to your original workflow. Automatically calculates and switches to the previous tab index.

**Args:**

- `wait` (WebDriverWait): WebDriverWait instance

**Returns:**

- None

**Examples:**

HTML:
```html
<a href="/details" target="_blank">View Details</a>
```

Python:
```python
from robo_appian.utils.BrowserUtils import BrowserUtils
from robo_appian.components import LinkUtils, LabelUtils

# Open details in new tab
LinkUtils.click(wait, "View Details")
BrowserUtils.switch_to_Tab(wait, 1)

# Read information from details page
LabelUtils.isLabelExists(wait, "Record Details")
# ... extract data ...

# Close details tab and return to main page
BrowserUtils.close_current_tab_and_switch_back(wait)

# Continue working in original tab
```

## Common Workflows

### Opening and Processing a New Tab

```python
from robo_appian.utils.BrowserUtils import BrowserUtils
from robo_appian.components import ButtonUtils, InputUtils

# Click button that opens new tab
ButtonUtils.clickByLabelText(wait, "Open Form")

# Switch to new tab
BrowserUtils.switch_to_Tab(wait, 1)

# Fill form in new tab
InputUtils.setValueByLabelText(wait, "Name", "John Doe")
ButtonUtils.clickByLabelText(wait, "Submit")

# Close new tab and return
BrowserUtils.close_current_tab_and_switch_back(wait)
```

### Handling Multiple Report Tabs

```python
from robo_appian.utils.BrowserUtils import BrowserUtils
from robo_appian.components.TableUtils import TableUtils

# Assume multiple report tabs are already open
tab_count = len(wait._driver.window_handles)

results = []
for tab_index in range(tab_count):
    BrowserUtils.switch_to_Tab(wait, tab_index)
    
    # Extract data from each tab
    table = TableUtils.findTableByColumnName(wait, "Amount")
    row_count = TableUtils.rowCount(table)
    
    results.append({
        'tab': tab_index,
        'title': wait._driver.title,
        'rows': row_count
    })

print(results)
```

### Verifying New Tab Contents

```python
from robo_appian.utils.BrowserUtils import BrowserUtils
from robo_appian.components import LinkUtils, LabelUtils

# Click link
LinkUtils.click(wait, "User Guide")

# Switch to new tab
BrowserUtils.switch_to_Tab(wait, 1)

# Verify expected content loaded
LabelUtils.isLabelExists(wait, "Getting Started")

# Close and return
BrowserUtils.close_current_tab_and_switch_back(wait)
```

### Cycling Through All Tabs

```python
from robo_appian.utils.BrowserUtils import BrowserUtils

# Process each tab in order
num_tabs = len(wait._driver.window_handles)

for i in range(num_tabs):
    print(f"Tab {i}: {wait._driver.title}")
    
    # Do work in this tab
    # ...
    
    # Move to next tab (wraps around at end)
    BrowserUtils.switch_to_next_tab(wait)
```

## Best Practices

### Track Tab Count

Always check how many tabs are open before switching:

```python
tab_count = len(wait._driver.window_handles)
if tab_count > 1:
    BrowserUtils.switch_to_Tab(wait, 1)
```

### Handle Tab Closure Gracefully

When closing tabs, ensure you're not closing the last tab:

```python
if len(wait._driver.window_handles) > 1:
    BrowserUtils.close_current_tab_and_switch_back(wait)
```

### Wait After Tab Switch

Give the browser time to switch context:

```python
from robo_appian.components.LabelUtils import LabelUtils

BrowserUtils.switch_to_Tab(wait, 1)

# Wait for content to confirm tab loaded
LabelUtils.isLabelExists(wait, "Expected Page Title")
```

### Clean Up Tabs in Test Teardown

Close extra tabs at the end of tests:

```python
def teardown():
    # Close all tabs except the first
    while len(wait._driver.window_handles) > 1:
        BrowserUtils.switch_to_Tab(wait, 1)
        wait._driver.close()
    
    # Return to first tab
    BrowserUtils.switch_to_Tab(wait, 0)
```