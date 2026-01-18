# Search Dropdown Utils

## Overview

SearchDropdownUtils provides methods to interact with search-enabled dropdown components in Appian. Search dropdowns allow users to type to filter available options before selecting. These components differ from standard dropdowns because they include a search input field. The utility automatically types the search term, waits for filtered options to populate, then clicks the matching option.

## Methods

### selectSearchDropdownValueByLabelText

Select a value from a search dropdown using exact label match.

Use this when you need to select from a searchable dropdown with a large number of options and you know the exact label text. This method clicks the dropdown, types the value into the search field to filter options, waits for the filtered list to appear, then clicks the matching option. Efficient for dropdowns with hundreds or thousands of options.

**Args:**

- `wait` (WebDriverWait): WebDriverWait instance with configured timeout
- `label` (str): Exact label text for the dropdown
- `value` (str): Exact text of the option to select

**Raises:**

- `TimeoutException`: If dropdown or option not found within timeout
- `ValueError`: If dropdown ID cannot be extracted

**Returns:** None

**Examples:**

HTML:
```html
<div>
  <span>Employee</span>
  <div role="combobox" id="employee_value">
    <span>Select...</span>
  </div>
</div>
<!-- After clicking -->
<input id="employee_searchInput" type="text" placeholder="Search..." />
<ul id="employee_list" role="listbox">
  <li><div>John Doe</div></li>
  <li><div>Jane Smith</div></li>
</ul>
```

Python:
```python
from robo_appian.components.SearchDropdownUtils import SearchDropdownUtils
from selenium.webdriver.support.ui import WebDriverWait

SearchDropdownUtils.selectSearchDropdownValueByLabelText(wait, "Employee", "John Doe")
```

---

### selectSearchDropdownValueByPartialLabelText

Select a value from a search dropdown using partial label match.

Use this when the dropdown label contains dynamic text or you only know part of the label. This method uses a contains match for the label, making it useful for labels with counters, dates, or other variable content.

**Args:**

- `wait` (WebDriverWait): WebDriverWait instance with configured timeout
- `label` (str): Partial label text (uses contains matching)
- `value` (str): Exact text of the option to select

**Raises:**

- `TimeoutException`: If dropdown or option not found within timeout
- `ValueError`: If dropdown ID cannot be extracted

**Returns:** None

**Examples:**

HTML:
```html
<div>
  <span>Employee (1,234 items)</span>
  <div role="combobox" id="employee_value">Select...</div>
</div>
```

Python:
```python
from robo_appian.components.SearchDropdownUtils import SearchDropdownUtils
from selenium.webdriver.support.ui import WebDriverWait

SearchDropdownUtils.selectSearchDropdownValueByPartialLabelText(wait, "Employee", "John Doe")
```