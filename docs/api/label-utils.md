# Label Utils

## Overview

LabelUtils provides methods to find and verify text labels, headings, and other text elements in Appian UI. Use LabelUtils to check for the presence of labels or text content that don't fit into form component categories. Useful for validation steps that verify page content, success messages, or error messages before or after actions.

## Methods

### isLabelExists

Check if a label or text element with exact text exists on the page.

Use this for non-blocking validation checks in test assertions or conditional logic. Returns False if the label is not found or times out, without raising an exception. Perfect for verifying success messages, error messages, or any text content that indicates a state or result.

**Args:**

- `wait` (WebDriverWait): WebDriverWait instance with configured timeout
- `label` (str): Exact visible text to search for

**Raises:** None (returns False instead of raising exceptions)

**Returns:** bool: True if label found and visible, False otherwise

**Examples:**

HTML:
```html
<div>
  <span>Success!</span>
  <p>Your form has been submitted.</p>
</div>

<div class="error-message">
  <strong>Error: Invalid input</strong>
</div>
```

Python:
```python
from robo_appian.components.LabelUtils import LabelUtils
from selenium.webdriver.support.ui import WebDriverWait

if LabelUtils.isLabelExists(wait, "Success!"):
    print("Form submitted successfully")

assert LabelUtils.isLabelExists(wait, "Your form has been submitted."), "Success message not found"
```

---

### clickByLabelText

Click a label or text element by its exact visible text.

Use this when you need to interact with text elements that trigger UI changes, such as collapsible section headers, expandable panels, or clickable labels. This method finds the element by its text and clicks it using reliable ActionChains interaction.

**Args:**

- `wait` (WebDriverWait): WebDriverWait instance with configured timeout
- `label` (str): Exact visible text of the element to click

**Raises:**

- `TimeoutException`: If element not found or not clickable within timeout

**Returns:** None

**Examples:**

HTML:
```html
<div class="collapsible-header" onclick="toggleSection()">
  <span>Expand Details</span>
</div>

<div class="clickable-label">
  <strong>Show More</strong>
</div>
```

Python:
```python
from robo_appian.components.LabelUtils import LabelUtils
from selenium.webdriver.support.ui import WebDriverWait

LabelUtils.clickByLabelText(wait, "Expand Details")
LabelUtils.clickByLabelText(wait, "Show More")
```

---

### isLabelExistsAfterLoad

Check if a label exists after explicitly waiting for it to become visible.

Use this for stricter validation that ensures the element is not only present in the DOM but also visible to the user. Unlike isLabelExists which may find hidden elements, this method waits for the element to become visible. Ideal for checking messages that appear after page loads or form submissions complete.

**Args:**

- `wait` (WebDriverWait): WebDriverWait instance with configured timeout
- `label` (str): Exact visible text to search for

**Raises:** None (returns False instead of raising exceptions)

**Returns:** bool: True if label becomes visible within timeout, False otherwise

**Examples:**

HTML:
```html
<!-- Initially hidden, becomes visible after AJAX call -->
<div id="success-message" style="display: none;">
  <span>Saved successfully</span>
</div>
```

Python:
```python
from robo_appian.components.LabelUtils import LabelUtils
from selenium.webdriver.support.ui import WebDriverWait

# Wait for success message to appear after form submission
if LabelUtils.isLabelExistsAfterLoad(wait, "Saved successfully"):
    print("Form saved and message displayed")
else:
    print("Success message did not appear")
```