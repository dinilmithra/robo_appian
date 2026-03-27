# Label Utils

`LabelUtils` checks and clicks visible text labels while skipping hidden content.

## Common Methods
- `clickByLabelText(page, label)`
- `isLabelExists(page, label)`

## Example
```python
if LabelUtils.isLabelExists(page, "Welcome"):
    LabelUtils.clickByLabelText(page, "Expand")
```
