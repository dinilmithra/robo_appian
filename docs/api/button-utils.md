# Button Utils

## Overview

ButtonUtils provides reliable button interactions using visible text labels. Buttons can be located by exact label match, partial text match, or HTML id attributes.

All click operations handle animations, overlays, and other timing issues automatically to ensure reliable interaction.

## Methods

### clickByLabelText

Click a button by its exact label text (full match).

Use this when you know the complete, exact text displayed on the button. This is the most precise way to interact with buttons and works best when button labels are stable and consistent across your application.

**Args:**

- `wait` (WebDriverWait): WebDriverWait instance
- `label` (str): Exact button label text to match

**Raises:**

- `TimeoutException`: If button not found or not clickable within wait timeout

**Examples:**

HTML:
```html
<button>
  <span>Submit</span>
</button>
```

Python:
```python
from robo_appian.components.ButtonUtils import ButtonUtils

# Click button with exact label "Submit"
ButtonUtils.clickByLabelText(wait, "Submit")
```

---

### clickByPartialLabelText

Click a button by partial label text match.

Use this when you only know part of the button text, or when button labels include dynamic content like counts or timestamps. This method uses a contains match, so "Save" will match "Save", "Save Draft", and "Draft and Save". Perfect for buttons with variable text.

**Args:**

- `wait` (WebDriverWait): WebDriverWait instance
- `label` (str): Partial button text (e.g., "Save" matches "Save", "Save Draft", and "Draft and Save")

**Raises:**

- `TimeoutException`: If button not found or not clickable within wait timeout

**Examples:**

HTML:
```html
<button>
  <span>Submit Application Form</span>
</button>
<button>
  <span>Save Draft</span>
</button>
```

Python:
```python
from robo_appian.components.ButtonUtils import ButtonUtils

# Matches "Submit Application Form" (contains "Application")
ButtonUtils.clickByPartialLabelText(wait, "Application")

# Matches "Save Draft" (contains "Draft")
ButtonUtils.clickByPartialLabelText(wait, "Draft")
```

---

### clickById

Click a button by its HTML id attribute.

Use this when the button has a specific HTML id and label-based selection isn't suitable. This is useful for buttons without visible text labels or when you need to target a specific button among several with similar labels.

**Args:**

- `wait` (WebDriverWait): WebDriverWait instance
- `id` (str): The HTML id attribute of the button element

**Raises:**

- `TimeoutException`: If button not found or not clickable within wait timeout

**Examples:**

HTML:
```html
<button id="save_button">
  <span>Save</span>
</button>
```

Python:
```python
from robo_appian.components.ButtonUtils import ButtonUtils

ButtonUtils.clickById(wait, "save_button")
```

---

### isButtonExistsByLabelText

Check if a button exists by exact label match.

Use this to verify a button is present on the page before attempting to click it. This method won't throw an error if the button is missing - it simply returns False. Perfect for conditional logic where button availability might vary based on user permissions or page state.

**Args:**

- `wait` (WebDriverWait): WebDriverWait instance
- `label` (str): Exact button label text to match

**Returns:**

- `bool`: True if button found, False otherwise

**Examples:**

HTML:
```html
<button>
  <span>Submit</span>
</button>
```

Python:
```python
from robo_appian.components.ButtonUtils import ButtonUtils

if ButtonUtils.isButtonExistsByLabelText(wait, "Submit"):
    ButtonUtils.clickByLabelText(wait, "Submit")
```

---

### isButtonExistsByPartialLabelText

Check if a button exists by partial label match.

Use this to verify a button containing specific text is present on the page. Like the exact match version, this returns a boolean without throwing errors. Useful when you need to check for buttons with dynamic or variable labels in conditional workflows.

**Args:**

- `wait` (WebDriverWait): WebDriverWait instance
- `label` (str): Partial button label text to match

**Returns:**

- `bool`: True if button found, False otherwise

**Examples:**

HTML:
```html
<button>
  <span>Save Changes</span>
</button>
```

Python:
```python
from robo_appian.components.ButtonUtils import ButtonUtils

if ButtonUtils.isButtonExistsByPartialLabelText(wait, "Save"):
    ButtonUtils.clickByPartialLabelText(wait, "Save")
```

---

### isButtonExistsByPartialLabelTextAfterLoad

Check if a button exists after page load by partial label match.

Use this when you need to verify a button appears after a page refresh, navigation, or asynchronous content load. This method waits for the page to complete loading before checking for the button, making it ideal for testing workflows that involve page transitions or dynamic UI updates.

**Args:**

- `wait` (WebDriverWait): WebDriverWait instance
- `label` (str): Partial button label text to match

**Returns:**

- `bool`: True if button found after page load, False otherwise

**Examples:**

HTML:
```html
<button>
  <span>Continue to Next Step</span>
</button>
```

Python:
```python
from robo_appian.components.ButtonUtils import ButtonUtils

if ButtonUtils.isButtonExistsByPartialLabelTextAfterLoad(wait, "Continue"):
    ButtonUtils.clickByPartialLabelText(wait, "Continue")
```

---

### waitForButtonToBeVisibleByPartialLabelText

Wait for a button to become visible by partial label match.

Use this when you need to wait for a button to appear on the page before proceeding. This is essential for handling dynamically loaded content or buttons that appear after asynchronous operations complete. The method blocks execution until the button is visible or the timeout is reached.

**Args:**

- `wait` (WebDriverWait): WebDriverWait instance
- `label` (str): Partial button label text to match

**Returns:**

- `WebElement`: The visible button element

**Raises:**

- `TimeoutException`: If button not visible within timeout

**Examples:**

HTML:
```html
<button>
  <span>Submit Application</span>
</button>
```

Python:
```python
from robo_appian.components.ButtonUtils import ButtonUtils

ButtonUtils.waitForButtonToBeVisibleByPartialLabelText(wait, "Submit")
ButtonUtils.clickByPartialLabelText(wait, "Submit")
```
