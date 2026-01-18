# Search Input Utils

## Overview

SearchInputUtils provides methods to interact with searchable input components in Appian. Similar to SearchDropdownUtils, but for input fields that support filtering and selection from a dropdown list. Use SearchInputUtils when you need to type into a search field and select a matching option from the results.

## Methods

### selectSearchDropdownByLabelText

Select a value from a search input using exact label match.

Use this when you need to search and select from an input field that provides autocomplete or filtered suggestions. This method types the search term into the input, waits for the listbox options to populate, then clicks the matching option. Common in Appian forms for employee selection, user lookup, or any searchable entity.

**Args:**

- `wait` (WebDriverWait): WebDriverWait instance with configured timeout
- `label` (str): Exact label text for the search input
- `value` (str): Exact text of the option to select from dropdown

**Raises:**

- `TimeoutException`: If input or option not found within timeout
- `ValueError`: If input does not have 'aria-controls' attribute

**Returns:** None

**Examples:**

HTML:
```html
<div>
  <span>Employee Name</span>
  <input role="combobox" aria-controls="employee_listbox" />
</div>
<!-- After typing -->
<ul id="employee_listbox" role="listbox">
  <li role="option"><div><div><div><div><div><div><p>John Doe</p></div></div></div></div></div></div></li>
  <li role="option"><div><div><div><div><div><div><p>John Smith</p></div></div></div></div></div></div></li>
</ul>
```

Python:
```python
from robo_appian.components.SearchInputUtils import SearchInputUtils
from selenium.webdriver.support.ui import WebDriverWait

SearchInputUtils.selectSearchDropdownByLabelText(wait, "Employee Name", "John Doe")
```

---

### selectSearchDropdownByPartialLabelText

Select a value from a search input using partial label match.

Use this when the search input label contains dynamic text or you only know part of the label. This method uses a contains match for the label, making it useful for labels with counters, dates, or other variable content. Otherwise behaves the same as selectSearchDropdownByLabelText.

**Args:**

- `wait` (WebDriverWait): WebDriverWait instance with configured timeout
- `label` (str): Partial label text (uses contains matching)
- `value` (str): Exact text of the option to select from dropdown

**Raises:**

- `TimeoutException`: If input or option not found within timeout
- `ValueError`: If input does not have 'aria-controls' attribute

**Returns:** None

**Examples:**

HTML:
```html
<div>
  <span>Employee (1,234 total)</span>
  <input role="combobox" aria-controls="employee_listbox" />
</div>
```

Python:
```python
from robo_appian.components.SearchInputUtils import SearchInputUtils
from selenium.webdriver.support.ui import WebDriverWait

SearchInputUtils.selectSearchDropdownByPartialLabelText(wait, "Employee", "John Doe")
```