# Table Utils

`TableUtils` locates Appian grid rows and cells by column name.

Public row numbers are zero-based. Internally the helpers convert to Appian's one-based `data-dnd-name` row identifiers.

## Common Methods
- `findTableByColumnName(page, column_name)`
- `rowCount(table)`
- `selectRowFromTableByColumnNameAndRowNumber(page, row_number, column_name)`
- `findComponentByColumnNameAndRowNumber(page, row_number, column_name)`
- `findComponentFromTableCell(page, row_number, column_name)`

## Example
```python
table = TableUtils.findTableByColumnName(page, "Employee ID")
assert TableUtils.rowCount(table) > 0
status_cell = TableUtils.findComponentByColumnNameAndRowNumber(page, 0, "Status")
```
