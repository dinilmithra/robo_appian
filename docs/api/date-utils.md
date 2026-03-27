# Date Utils

`DateUtils` fills Appian date inputs by visible label.

## Common Methods
- `setValueByLabelText(page, label, value)`
- `clickByLabelText(page, label)`

Dates should be provided in `MM/DD/YYYY` format.

## Example
```python
DateUtils.setValueByLabelText(page, "Start Date", "01/15/2026")
DateUtils.clickByLabelText(page, "End Date")
```
