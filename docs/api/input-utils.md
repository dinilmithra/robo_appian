# Input Utils

`InputUtils` fills Appian text inputs through label-driven locators.

## Common Methods
- `setValueByLabelText(page, label, value)`
- `setValueByPartialLabelText(page, label, value)`
- `setValueById(page, id, value)`
- `setValueByPlaceholderText(page, placeholder, value)`

## Example
```python
InputUtils.setValueByLabelText(page, "Username", "demo_user")
InputUtils.setValueByPlaceholderText(page, "Search", "invoice 123")
```
