# Dropdown Utils

`DropdownUtils` works with Appian combobox-based dropdowns.

## Common Methods
- `selectDropdownValueByLabelText(page, label, value)`
- `selectDropdownValueByPartialLabelText(page, label, value)`
- `selectDropdownValueByComboboxComponent(page, combobox, value)`
- `checkEditableStatusByLabelText(page, label)`
- `checkReadOnlyStatusByLabelText(page, label)`
- `getDropdownOptionValues(page, label)`

## Example
```python
DropdownUtils.selectDropdownValueByLabelText(page, "Status", "Active")
values = DropdownUtils.getDropdownOptionValues(page, "Status")
```
