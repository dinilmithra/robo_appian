# Search Input Utils

`SearchInputUtils` types into searchable Appian inputs and selects from the resulting listbox.

## Common Methods
- `selectSearchInputByLabelText(page, label, value)`
- `selectSearchInputByPartialLabelText(page, label, value)`

Backward-compatible aliases `selectSearchDropdownByLabelText` and `selectSearchDropdownByPartialLabelText` remain available.

## Example
```python
SearchInputUtils.selectSearchInputByLabelText(page, "Employee", "John Doe")
```
