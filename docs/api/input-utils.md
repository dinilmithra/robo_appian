# Input Utils

## Overview

InputUtils provides reliable text input interactions using visible label text. Inputs can be located by exact label match, partial label match, HTML id attributes, or placeholder text.

All input operations handle timing issues automatically and clear existing values before entering new text.

## Methods

### setValueByLabelText

Set value in an input field by its exact label text.

Use this when you know the complete, exact label text associated with the input field. This is the most precise way to interact with inputs and works best when label text is stable and consistent across your application.

**Args:**

- `wait` (WebDriverWait): WebDriverWait instance
- `label` (str): Exact visible label text to match
- `value` (str): Text to enter into the input field

**Raises:**

- `ValueError`: If label element has no 'for' attribute linking to input
- `TimeoutException`: If label or input not found within timeout

**Examples:**

HTML:
```html
<div>
  <label for="username_input">Username</label>
  <input id="username_input" type="text" />
</div>
```

Python:
```python
from robo_appian.components.InputUtils import InputUtils

InputUtils.setValueByLabelText(wait, "Username", "john_doe")
```

---

### setValueByPartialLabelText

Set value in an input field by partial label match.

Use this when you only know part of the label text, or when labels include dynamic content. Perfect for situations where the full label might change but a key word remains constant (e.g., "Name" appears in "First Name", "User Name", etc.).

**Args:**

- `wait` (WebDriverWait): WebDriverWait instance
- `label` (str): Partial label text to match
- `value` (str): Text to enter into the input field

**Raises:**

- `ValueError`: If label element has no 'for' attribute linking to input
- `TimeoutException`: If label or input not found within timeout

**Examples:**

HTML:
```html
<div>
  <label for="first_name_input">First Name</label>
  <input id="first_name_input" type="text" />
</div>
```

Python:
```python
from robo_appian.components.InputUtils import InputUtils

# Matches "First Name", "User Name", "Full Name", etc.
InputUtils.setValueByPartialLabelText(wait, "Name", "John")
```

---

### setValueById

Set value in an input field by its HTML id attribute.

Use this when the input has a specific HTML id and label-based selection isn't suitable. This is useful for inputs without visible labels or when you need to target a specific field among several with similar labels.

**Args:**

- `wait` (WebDriverWait): WebDriverWait instance
- `id` (str): The HTML id attribute of the input element
- `value` (str): Text to enter into the input field

**Raises:**

- `TimeoutException`: If input not found within timeout

**Examples:**

HTML:
```html
<input id="email_input" type="email" />
```

Python:
```python
from robo_appian.components.InputUtils import InputUtils

InputUtils.setValueById(wait, "email_input", "user@example.com")
```

---

### setValueByPlaceholderText

Set value in an input field by its placeholder text.

Use this when the input field has placeholder text but no visible label. Placeholder text is the hint text that appears inside an empty input field (e.g., "Enter your email").

**Args:**

- `wait` (WebDriverWait): WebDriverWait instance
- `text` (str): The placeholder text of the input field
- `value` (str): Text to enter into the input field

**Raises:**

- `TimeoutException`: If input not found within timeout

**Examples:**

HTML:
```html
<input type="email" placeholder="Enter your email" />
```

Python:
```python
from robo_appian.components.InputUtils import InputUtils

InputUtils.setValueByPlaceholderText(wait, "Enter your email", "user@example.com")
```