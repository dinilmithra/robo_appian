# Table Operations

Interact with Appian grid components by column name and row index (0-based in APIs).

## Basic Table Interactions

```python
from robo_appian.components import TableUtils, ButtonUtils

# Click the first row where column "Employee ID" is present
TableUtils.selectRowFromTableByColumnNameAndRowNumber(wait, 0, "Employee ID")

# Click a button inside a cell
cell_component = TableUtils.findComponentFromTableCell(wait, 0, "Actions")
ButtonUtils.clickByLabelText(wait, "Edit")

# Read a component from a specific column/row
status_cell = TableUtils.findComponentByColumnNameAndRowNumber(wait, 1, "Status")
text = status_cell.text
```

## Count and Iterate Through Rows

```python
from robo_appian.components import TableUtils

# Find table and get row count
table = TableUtils.findTableByColumnName(wait, "Employee ID")
row_count = TableUtils.rowCount(table)

print(f"Table has {row_count} rows")

# Iterate through all rows
for row_index in range(row_count):
    # Get cell value from each row
    name_cell = TableUtils.findComponentByColumnNameAndRowNumber(wait, row_index, "Name")
    print(f"Row {row_index}: {name_cell.text}")
```

## Find and Click Specific Row

```python
from robo_appian.components import TableUtils

# Find table
table = TableUtils.findTableByColumnName(wait, "Status")
row_count = TableUtils.rowCount(table)

# Search for row with specific value
for row_index in range(row_count):
    status = TableUtils.findComponentByColumnNameAndRowNumber(wait, row_index, "Status")
    
    if status.text == "Pending":
        # Click action button in this row
        TableUtils.selectRowFromTableByColumnNameAndRowNumber(wait, row_index, "Status")
        break
```

## Extract All Data from Table

```python
from robo_appian.components import TableUtils

# Get table reference
table = TableUtils.findTableByColumnName(wait, "Employee ID")
row_count = TableUtils.rowCount(table)

# Define columns to extract
columns = ["Employee ID", "Name", "Department", "Status"]

# Extract all data
table_data = []
for row_index in range(row_count):
    row_data = {}
    for column in columns:
        cell = TableUtils.findComponentByColumnNameAndRowNumber(wait, row_index, column)
        row_data[column] = cell.text
    table_data.append(row_data)

# Use extracted data
for row in table_data:
    print(f"{row['Name']} - {row['Department']} - {row['Status']}")
```

## Click Button in Specific Cell

```python
from robo_appian.components import TableUtils, ButtonUtils

# Find and click the Edit button in row 2, Actions column
edit_button = TableUtils.findComponentFromTableCell(wait, 2, "Actions")
ComponentUtils.click(wait, edit_button)

# Or if the button has a label, click by label
TableUtils.findComponentFromTableCell(wait, 2, "Actions")
ButtonUtils.clickByLabelText(wait, "Delete")
```

## Verify Table Contents

```python
from robo_appian.components import TableUtils

# Find specific employee row
table = TableUtils.findTableByColumnName(wait, "Name")
row_count = TableUtils.rowCount(table)

# Verify specific employee exists
employee_found = False
for row_index in range(row_count):
    name_cell = TableUtils.findComponentByColumnNameAndRowNumber(wait, row_index, "Name")
    if name_cell.text == "John Doe":
        employee_found = True
        
        # Verify other columns for this employee
        status = TableUtils.findComponentByColumnNameAndRowNumber(wait, row_index, "Status")
        assert status.text == "Active", f"Expected Active but got {status.text}"
        break

assert employee_found, "Employee 'John Doe' not found in table"
```

## Handle Paginated Tables

```python
from robo_appian.components import TableUtils, ButtonUtils, LabelUtils

# Process all pages
while True:
    # Process current page
    table = TableUtils.findTableByColumnName(wait, "Employee ID")
    row_count = TableUtils.rowCount(table)
    
    for row_index in range(row_count):
        # Process each row
        cell = TableUtils.findComponentByColumnNameAndRowNumber(wait, row_index, "Name")
        print(f"Processing: {cell.text}")
    
    # Check if "Next" button exists and is enabled
    try:
        ButtonUtils.clickByLabelText(wait, "Next")
    except:
        # No more pages
        break
```

Guidelines:
- Column detection uses header `abbr` attributes; ensure your column names match those values.
- Public APIs use 0-based row numbers; the helper converts to Appian's 1-based row identifiers.
- Empty grid rows are skipped via `data-empty-grid-message` checks.
- For large tables, consider extracting data in batches to avoid memory issues.
