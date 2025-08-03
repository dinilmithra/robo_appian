# SearchInputUtils

The `SearchInputUtils` class provides utility methods for interacting with Appian's search input and search dropdown components. It enables automation of entering values and selecting options in search-enabled fields.

## Overview

SearchInputUtils is designed to:
- Select values from search dropdowns by exact or partial label
- Automate search input field interactions in Appian UIs
- Handle dynamic dropdowns and search suggestions

## Import
```python
from robo_appian.components.SearchInputUtils import SearchInputUtils
```

## Class Methods

### selectSearchDropdownByLabelText()
Selects a value from a search dropdown by matching the exact label text.

**Parameters:**
- `wait` (`WebDriverWait`): Selenium WebDriverWait instance
- `label` (`str`): The exact visible label of the search input
- `value` (`str`): The value to select from the dropdown

**Usage Example:**
```python
SearchInputUtils.selectSearchDropdownByLabelText(wait, "Country", "India")
```

### selectSearchDropdownByPartialLabelText()
Selects a value from a search dropdown by matching partial label text.

**Parameters:**
- `wait` (`WebDriverWait`): Selenium WebDriverWait instance
- `label` (`str`): Partial label text of the search input
- `value` (`str`): The value to select from the dropdown

**Usage Example:**
```python
SearchInputUtils.selectSearchDropdownByPartialLabelText(wait, "Coun", "India")
```

## How It Works
- Locates the search input field by its label (exact or partial)
- Enters the desired value
- Waits for the dropdown options to appear
- Selects the matching option from the dropdown

## Error Handling
- Raises `TimeoutError` if the dropdown option is not found
- Raises `ValueError` if the search input component is not found or is misconfigured

## See Also
- [InputUtils](input-utils.md)
- [DropdownUtils](dropdown-utils.md)
