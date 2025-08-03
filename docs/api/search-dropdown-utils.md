# SearchDropdownUtils API Reference

The `SearchDropdownUtils` class provides utility methods for interacting with Appian's search dropdown components. These utilities help automate the process of selecting options from search-enabled dropdowns by label or partial label.

## Import
```python
from robo_appian.components.SearchDropdownUtils import SearchDropdownUtils
```

## Methods

### selectSearchDropdownValueByLabelText

Selects a value from a search dropdown by matching the exact label text.

**Syntax:**
```python
SearchDropdownUtils.selectSearchDropdownValueByLabelText(wait, dropdown_label, value)
```
**Parameters:**
- `wait` (WebDriverWait): Selenium WebDriverWait instance
- `dropdown_label` (str): The exact visible label of the search dropdown
- `value` (str): The value to select from the dropdown

**Example:**
```python
SearchDropdownUtils.selectSearchDropdownValueByLabelText(wait, "Status", "Approved")
```

### selectSearchDropdownValueByPartialLabelText

Selects a value from a search dropdown by matching partial label text.

**Syntax:**
```python
SearchDropdownUtils.selectSearchDropdownValueByPartialLabelText(wait, dropdown_label, value)
```
**Parameters:**
- `wait` (WebDriverWait): Selenium WebDriverWait instance
- `dropdown_label` (str): Partial label text of the search dropdown
- `value` (str): The value to select from the dropdown

**Example:**
```python
SearchDropdownUtils.selectSearchDropdownValueByPartialLabelText(wait, "Stat", "Approved")
```

## How it Works
- Locates the search dropdown by its label (exact or partial)
- Clicks the dropdown to activate the search input
- Enters the desired value
- Waits for the dropdown options to appear
- Selects the matching option from the dropdown

## Error Handling
- Raises `RuntimeError` if the dropdown or option is not found or not clickable

## See Also
- [InputUtils](input-utils.md)
- [DropdownUtils](dropdown-utils.md)
