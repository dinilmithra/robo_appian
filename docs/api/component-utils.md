# Component Utils

## Overview

ComponentUtils provides foundational capabilities for interacting with web elements. These low-level utilities handle element waiting, clicking, visibility checks, and date formatting.

Most robo_appian components use ComponentUtils internally. You can also use these methods directly for custom interactions not covered by higher-level utilities.

## Methods

### click

Reliably click an element using ActionChains with automatic waiting.

Use this instead of `element.click()` for more reliable clicks that handle animations, overlays, and timing issues. This method waits for the element to be clickable, moves the mouse to it, and performs a safe click.

**Args:**

- `wait` (WebDriverWait): WebDriverWait instance
- `component` (WebElement): The element to click

**Raises:**

- `TimeoutException`: If element not clickable within timeout

**Examples:**

HTML:
```html
<button id="save_btn">
  <span>Save</span>
</button>
```

Python:
```python
from robo_appian.utils.ComponentUtils import ComponentUtils
from selenium.webdriver.common.by import By

# Find element and click safely
button = driver.find_element(By.ID, "save_btn")
ComponentUtils.click(wait, button)
```

---

### waitForComponentToBeVisibleByXpath

Wait for an element to become visible and return it.

Use this when you need to find an element by XPath and ensure it's both present in the DOM and visible to users before proceeding. This is used internally by most robo_appian utilities.

**Args:**

- `wait` (WebDriverWait): WebDriverWait instance
- `xpath` (str): XPath expression to locate the element

**Returns:**

- `WebElement`: The element once it becomes visible

**Raises:**

- `TimeoutException`: If element not visible within timeout

**Examples:**

HTML:
```html
<div id="status">
  <span>Loading complete</span>
</div>
```

Python:
```python
from robo_appian.utils.ComponentUtils import ComponentUtils

# Wait for status message
element = ComponentUtils.waitForComponentToBeVisibleByXpath(
    wait, 
    "//span[text()='Loading complete']"
)
print(element.text)  # "Loading complete"
```

---

### waitForComponentNotToBeVisibleByXpath

Wait until an element is no longer visible.

Use this when you need to verify an element has disappeared, such as waiting for a loading spinner to finish or a modal dialog to close.

**Args:**

- `wait` (WebDriverWait): WebDriverWait instance
- `xpath` (str): XPath expression to locate the element

**Returns:**

- `bool`: True if element became invisible before timeout

**Raises:**

- `TimeoutException`: If element still visible after timeout

**Examples:**

HTML:
```html
<!-- Initially visible, then hidden -->
<div class="spinner">Loading...</div>
```

Python:
```python
from robo_appian.utils.ComponentUtils import ComponentUtils

# Wait for loading spinner to disappear
ComponentUtils.waitForComponentNotToBeVisibleByXpath(
    wait, 
    "//div[@class='spinner']"
)
# Continue with next action after spinner is gone
```

---

### waitForElementToBeVisibleById

Wait for an element with a specific ID to become visible.

Use this when elements have unique HTML id attributes. Simpler than XPath for straightforward element identification.

**Args:**

- `wait` (WebDriverWait): WebDriverWait instance
- `id` (str): The HTML id attribute value

**Returns:**

- `WebElement`: The element once visible

**Raises:**

- `TimeoutException`: If element not visible within timeout

**Examples:**

HTML:
```html
<div id="success_message">
  Form submitted successfully
</div>
```

Python:
```python
from robo_appian.utils.ComponentUtils import ComponentUtils

# Wait for success message by ID
element = ComponentUtils.waitForElementToBeVisibleById(wait, "success_message")
print(element.text)
```

---

### waitForElementNotToBeVisibleById

Wait until an element with a specific ID is no longer visible.

Use this to verify an element has been removed or hidden, using its ID attribute.

**Args:**

- `wait` (WebDriverWait): WebDriverWait instance
- `id` (str): The HTML id attribute value

**Returns:**

- `bool`: True if element became invisible

**Raises:**

- `TimeoutException`: If element still visible after timeout

**Examples:**

HTML:
```html
<div id="loading_overlay">Please wait...</div>
```

Python:
```python
from robo_appian.utils.ComponentUtils import ComponentUtils

# Wait for overlay to disappear
ComponentUtils.waitForElementNotToBeVisibleById(wait, "loading_overlay")
```

---

### waitForElementToBeVisibleByText

Wait for an element containing specific text to become visible.

Use this when you need to find elements by their visible text content, regardless of their HTML structure or attributes.

**Args:**

- `wait` (WebDriverWait): WebDriverWait instance
- `text` (str): Exact text content to match

**Returns:**

- `WebElement`: The element containing the text

**Raises:**

- `TimeoutException`: If element not visible within timeout

**Examples:**

HTML:
```html
<div class="notification">
  <p>Your changes have been saved</p>
</div>
```

Python:
```python
from robo_appian.utils.ComponentUtils import ComponentUtils

# Wait for specific text to appear
element = ComponentUtils.waitForElementToBeVisibleByText(
    wait, 
    "Your changes have been saved"
)
```

---

### waitForElementNotToBeVisibleByText

Wait until an element with specific text is no longer visible.

Use this to verify that messages, notifications, or other text-based elements have disappeared.

**Args:**

- `wait` (WebDriverWait): WebDriverWait instance
- `text` (str): Exact text content to match

**Returns:**

- `bool`: True if element became invisible

**Raises:**

- `TimeoutException`: If element still visible after timeout

**Examples:**

HTML:
```html
<div class="toast-message">Processing...</div>
```

Python:
```python
from robo_appian.utils.ComponentUtils import ComponentUtils

# Wait for processing message to disappear
ComponentUtils.waitForElementNotToBeVisibleByText(wait, "Processing...")
```

---

### findComponentById

Find and return an element by its ID attribute.

Use this when you need to locate an element by ID and wait for it to be present in the DOM (but not necessarily visible).

**Args:**

- `wait` (WebDriverWait): WebDriverWait instance
- `id` (str): The HTML id attribute value

**Returns:**

- `WebElement`: The located element

**Raises:**

- `TimeoutException`: If element not found within timeout

**Examples:**

HTML:
```html
<input id="username_field" type="text" />
```

Python:
```python
from robo_appian.utils.ComponentUtils import ComponentUtils

# Find element by ID
input_field = ComponentUtils.findComponentById(wait, "username_field")
input_field.send_keys("test_user")
```

---

### checkComponentExistsByXpath

Check if a component exists without throwing an exception.

Use this when you want to conditionally perform actions based on element presence, such as closing optional dialogs or handling dynamic UI elements.

**Args:**

- `wait` (WebDriverWait): WebDriverWait instance
- `xpath` (str): XPath expression to locate the element

**Returns:**

- `bool`: True if element exists and is visible, False otherwise

**Examples:**

HTML:
```html
<!-- Optional cookie banner -->
<div id="cookie_banner">
  <button>Accept Cookies</button>
</div>
```

Python:
```python
from robo_appian.utils.ComponentUtils import ComponentUtils

# Check if cookie banner exists before dismissing
if ComponentUtils.checkComponentExistsByXpath(wait, "//div[@id='cookie_banner']"):
    # Close the banner
    ComponentUtils.findComponentUsingXpathAndClick(wait, "//button[text()='Accept Cookies']")
```

---

### findCount

Count the number of elements matching an XPath expression.

Use this to determine how many elements match a pattern, such as counting table rows, list items, or validation errors.

**Args:**

- `wait` (WebDriverWait): WebDriverWait instance
- `xpath` (str): XPath expression to locate elements

**Returns:**

- `int`: Number of matching elements (0 if none found)

**Examples:**

HTML:
```html
<ul class="item-list">
  <li class="item">Item 1</li>
  <li class="item">Item 2</li>
  <li class="item">Item 3</li>
</ul>
```

Python:
```python
from robo_appian.utils.ComponentUtils import ComponentUtils

# Count list items
count = ComponentUtils.findCount(wait, "//li[@class='item']")
print(f"Found {count} items")  # "Found 3 items"
```

---

### tab

Simulate a Tab key press.

Use this to navigate between form fields using keyboard navigation, which can be more reliable than clicking in certain Appian forms.

**Args:**

- `wait` (WebDriverWait): WebDriverWait instance

**Returns:**

- None

**Examples:**

Python:
```python
from robo_appian.utils.ComponentUtils import ComponentUtils
from robo_appian.components.InputUtils import InputUtils

# Fill first field
InputUtils.setValueByLabelText(wait, "First Name", "John")

# Tab to next field
ComponentUtils.tab(wait)

# Continue with next field
InputUtils.setValueByLabelText(wait, "Last Name", "Doe")
```

---

### today

Get today's date formatted as MM/DD/YYYY.

Use this for populating date fields with the current date in Appian's expected format.

**Args:**

- None

**Returns:**

- `str`: Today's date in MM/DD/YYYY format

**Examples:**

Python:
```python
from robo_appian.utils.ComponentUtils import ComponentUtils
from robo_appian.components.DateUtils import DateUtils

# Set date field to today
today_date = ComponentUtils.today()
DateUtils.setValueByLabelText(wait, "Submission Date", today_date)
```

---

### yesterday

Get yesterday's date formatted as MM/DD/YYYY.

Use this for populating date fields with yesterday's date, useful for testing date range filters or historical data entry.

**Args:**

- None

**Returns:**

- `str`: Yesterday's date in MM/DD/YYYY format

**Examples:**

Python:
```python
from robo_appian.utils.ComponentUtils import ComponentUtils
from robo_appian.components.DateUtils import DateUtils

# Set start date to yesterday
yesterday_date = ComponentUtils.yesterday()
DateUtils.setValueByLabelText(wait, "Start Date", yesterday_date)
```

---

### get_version

Get the current version of robo_appian from pyproject.toml.

Use this for logging, diagnostics, or version compatibility checks in your test framework.

**Args:**

- None

**Returns:**

- `str`: Version string (e.g., "0.0.33") or "0.0.0" if unable to read

**Examples:**

Python:
```python
from robo_appian.utils.ComponentUtils import ComponentUtils

# Log version in test setup
version = ComponentUtils.get_version()
print(f"Running tests with robo_appian v{version}")
```