# Button Utils

`ButtonUtils` clicks Appian buttons by visible text.

## Common Methods
- `clickByLabelText(page, label)`
- `clickByPartialLabelText(page, label)`
- `clickById(page, id)`
- `isButtonExistsByLabelText(page, label)`
- `isButtonExistsByPartialLabelText(page, label)`

## Example
```python
ButtonUtils.clickByLabelText(page, "Submit")
ButtonUtils.clickByPartialLabelText(page, "Save")
```
