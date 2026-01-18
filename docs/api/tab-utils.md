# Tab Utils

## Overview

TabUtils provides methods to select and interact with tab components in Appian UI. Use TabUtils to navigate between different sections within a single page. Tabs are commonly used in Appian to organize related content, and clicking a tab triggers content reloads in the tab panel.

## Methods

### selectTabByLabelText

Click a tab to navigate to it by its exact visible label.

Use this when you need to switch between different tab sections in an Appian interface. After clicking the tab, content within the tab panel will load, so be ready to wait for elements within the new tab section before interacting with them.

**Args:**

- `wait` (WebDriverWait): WebDriverWait instance with configured timeout
- `label` (str): Exact visible label text of the tab to select

**Raises:**

- `TimeoutException`: If tab not found or not clickable within timeout

**Returns:** None

**Examples:**

HTML:
```html
<div class="tabs">
  <div role="link">
    <div><div><div><div><div><p>Details</p></div></div></div></div></div>
  </div>
  <div role="link">
    <div><div><div><div><div><p>History</p></div></div></div></div></div>
  </div>
</div>
```

Python:
```python
from robo_appian.components.TabUtils import TabUtils
from selenium.webdriver.support.ui import WebDriverWait

TabUtils.selectTabByLabelText(wait, "Details")
```

---

### findTabByLabelText

Find a tab element by its exact visible label without clicking it.

Use this when you need to inspect a tab element or perform custom operations on it before clicking. Returns the tab WebElement for advanced use cases like checking attributes, getting position, or chaining operations. Most commonly you'll use selectTabByLabelText instead, but this is useful for validation or custom interactions.

**Args:**

- `wait` (WebDriverWait): WebDriverWait instance with configured timeout
- `label` (str): Exact visible label text of the tab

**Raises:**

- `TimeoutException`: If tab not found within timeout

**Returns:** WebElement representing the tab element

**Examples:**

HTML:
```html
<div class="tabs">
  <div role="link">
    <div><div><div><div><div><p>Details</p></div></div></div></div></div>
  </div>
</div>
```

Python:
```python
from robo_appian.components.TabUtils import TabUtils
from selenium.webdriver.support.ui import WebDriverWait

tab = TabUtils.findTabByLabelText(wait, "Details")
print(f"Tab text: {tab.text}")
```

---

### checkTabSelectedByLabelText

Check if a specific tab is currently selected (active).

Use this to verify that navigation to a tab was successful, or to check the current active tab state in test assertions. Returns True if the tab has the "Selected Tab" indicator, False otherwise. Useful for confirming that clicking a tab actually activated it before interacting with tab content.

**Args:**

- `wait` (WebDriverWait): WebDriverWait instance with configured timeout
- `label` (str): Exact visible label text of the tab to check

**Raises:** None (returns False if tab not found or not selected)

**Returns:** bool: True if tab is currently selected, False otherwise

**Examples:**

HTML:
```html
<div role="link">
  <div><div><div><div><div>
    <p>Details</p>
    <span>Selected Tab.</span>
  </div></div></div></div></div>
</div>

<div role="link">
  <div><div><div><div><div>
    <p>History</p>
  </div></div></div></div></div>
</div>
```

Python:
```python
from robo_appian.components.TabUtils import TabUtils
from selenium.webdriver.support.ui import WebDriverWait

TabUtils.selectTabByLabelText(wait, "Details")

if TabUtils.checkTabSelectedByLabelText(wait, "Details"):
    print("Details tab is now active")

assert TabUtils.checkTabSelectedByLabelText(wait, "Details"), "Details tab should be selected"
```