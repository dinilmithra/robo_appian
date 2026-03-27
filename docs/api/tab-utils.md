# Tab Utils

`TabUtils` locates, clicks, and verifies Appian tabs.

## Common Methods
- `findTabByLabelText(page, label)`
- `selectTabByLabelText(page, label)`
- `checkTabSelectedByLabelText(page, label)`

## Example
```python
TabUtils.selectTabByLabelText(page, "History")
assert TabUtils.checkTabSelectedByLabelText(page, "History") is True
```
