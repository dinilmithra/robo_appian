# Date Utils

## Overview

DateUtils provides methods to interact with Appian date picker components. Use DateUtils to fill date fields by their label, clear existing dates, or click to open calendar pickers. All date values should be formatted as MM/DD/YYYY to match Appian's expected format.

## Methods

### setValueByLabelText

Set a date value in a date picker by its associated label.

Use this when you need to fill a date field and you know the exact label text displayed next to or above the date picker. This method automatically waits for the date input to be clickable, clears any existing value, and enters the new date. Perfect for form submissions where dates are required fields.

**Args:**

- `wait` (WebDriverWait): WebDriverWait instance with configured timeout
- `label` (str): Exact label text for the date picker
- `value` (str): Date string in MM/DD/YYYY format (e.g., "01/15/2024")

**Raises:**

- `TimeoutException`: If date picker not found or not clickable within timeout

**Returns:**

- WebElement representing the date input component

**Examples:**

HTML:
```html
<div>
  <label>End Date</label>
  <input type="text" class="date-picker" placeholder="MM/DD/YYYY" />
</div>
```

Python:
```python
from robo_appian.components.DateUtils import DateUtils
from selenium.webdriver.support.ui import WebDriverWait

DateUtils.setValueByLabelText(wait, "End Date", "12/31/2024")
```

---

### clickByLabelText

Click on a date picker field to open the calendar popup.

Use this when you need to interact with the date picker's calendar interface rather than typing a date directly. This opens the visual calendar widget where users can select dates by clicking on days. Useful for exploring date selections or when the date picker requires calendar interaction for validation.

**Args:**

- `wait` (WebDriverWait): WebDriverWait instance with configured timeout
- `label` (str): Exact label text for the date picker

**Raises:**

- `TimeoutException`: If date picker not found or not clickable within timeout

**Returns:**

- WebElement representing the date input component

**Examples:**

HTML:
```html
<div>
  <label>Event Date</label>
  <input type="text" class="date-picker" placeholder="MM/DD/YYYY" />
  <!-- Clicking input opens calendar popup -->
</div>
```

Python:
```python
from robo_appian.components.DateUtils import DateUtils
from selenium.webdriver.support.ui import WebDriverWait

# Click to open the calendar picker
DateUtils.clickByLabelText(wait, "Event Date")
# Calendar popup appears for visual date selection
```