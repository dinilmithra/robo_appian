# Search Dropdown Utils

`SearchDropdownUtils` types into Appian search dropdowns and selects a matching result.

## Common Methods
- `selectSearchDropdownValueByLabelText(page, label, value)`
- `selectSearchDropdownValueByPartialLabelText(page, label, value)`

## Example
```python
SearchDropdownUtils.selectSearchDropdownValueByLabelText(
    page,
    "Approver",
    "Jane Smith",
)
```
