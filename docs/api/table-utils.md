# TableUtils

The `TableUtils` class provides comprehensive methods for interacting with table components in Appian applications. It handles the complex operations required for data table interactions, including finding tables, counting rows, and locating specific cell components.

## Overview

TableUtils is designed to handle Appian's data table structures, providing reliable methods to:

- Find tables by column names
- Count table rows (excluding empty rows)
- Locate specific cell components by row and column
- Extract data from table cells
- Navigate complex table hierarchies

## Class Methods
**Signature:**
```python
@staticmethod
def findTableByColumnName(wait: WebDriverWait, columnName: str) -> WebElement
```

### findTableByColumnName()

**Signature:**
@staticmethod
def findTableByColumnName(wait: WebDriverWait, columnName: str) -> WebElement
```

**Parameters:**
- `wait` (WebDriverWait): Selenium WebDriverWait instance for element waiting
- `columnName` (str): The name of the column to search for in table headers

**Returns:**
- `WebElement`: The table element containing the specified column

**Usage Example:**
```python
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from robo_appian.components.TableUtils import TableUtils

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

table = TableUtils.findTableByColumnName(wait, "Employee ID")

# Find table with status column
status_table = TableUtils.findTableByColumnName(wait, "Status")


### rowCount()
Counts the number of data rows in a table, excluding empty rows and header rows.

```python
@staticmethod
def rowCount(tableObject: WebElement) -> int
```

**Parameters:**
- `tableObject` (WebElement): The table WebElement to count rows in

**Returns:**
- `int`: The number of data rows in the table

**Usage Example:**
```python
# Get table and count rows
table = TableUtils.findTableByColumnName(wait, "Employee ID")
row_count = TableUtils.rowCount(table)
print(f"Table contains {row_count} rows")

# Use row count for iteration
for i in range(row_count):
    # Process each row
**Signature:**
```python
@staticmethod
def findComponentFromTableCell(wait: WebDriverWait, rowNumber: int, columnName: str) -> WebElement
```
    cell_component = TableUtils.findComponentFromTableCell(wait, i, "Status")
    # Perform operations on cell component

### findComponentFromTableCell()
Finds a component within a specific table cell by row number and column name.

**Signature:**
```python
@staticmethod
def findComponentFromTableCell(wait: WebDriverWait, rowNumber: int, columnName: str) -> WebElement
```

**Parameters:**
- `wait` (WebDriverWait): Selenium WebDriverWait instance for element waiting
- `rowNumber` (int): The row number (0-based index) to search in
- `columnName` (str): The name of the column to search in

**Returns:**
- `WebElement`: The component found in the specified table cell

**Usage Example:**
```python
# Find component in first row, Status column
status_component = TableUtils.findComponentFromTableCell(wait, 0, "Status")

# Find component in third row, Name column
name_component = TableUtils.findComponentFromTableCell(wait, 2, "Employee Name")

# Find and interact with button in specific cell
button_component = TableUtils.findComponentFromTableCell(wait, 1, "Actions")
button_component.click()

# Find and get text from specific cell
text_component = TableUtils.findComponentFromTableCell(wait, 0, "Department")
department_text = text_component.text
```

## Best Practices

### Table Identification

**Use unique column names** for reliable table identification:
```python
# ✅ Recommended - unique column identifier
table = TableUtils.findTableByColumnName(wait, "Employee ID")

# ❌ Less reliable - common column name might match multiple tables
table = TableUtils.findTableByColumnName(wait, "Name")
```

### Row Iteration

**Always check row count** before iterating:
```python
table = TableUtils.findTableByColumnName(wait, "Employee ID")
row_count = TableUtils.rowCount(table)

if row_count > 0:
    for i in range(row_count):
        # Process each row safely
        component = TableUtils.findComponentFromTableCell(wait, i, "Status")
        # Perform operations
else:
    print("Table is empty")
```

### Error Handling

**Wrap table operations** in try-catch blocks:
```python
try:
    table = TableUtils.findTableByColumnName(wait, "Employee ID")
    row_count = TableUtils.rowCount(table)
    
    for i in range(row_count):
        try:
            component = TableUtils.findComponentFromTableCell(wait, i, "Status")
            # Process component
        except Exception as e:
            print(f"Error processing row {i}: {e}")
            continue
            
except Exception as e:
    print(f"Error finding or processing table: {e}")
```

## Common Use Cases

### Data Validation
```python
# Validate all employees have active status
table = TableUtils.findTableByColumnName(wait, "Employee ID")
row_count = TableUtils.rowCount(table)

inactive_employees = []
for i in range(row_count):
    status_component = TableUtils.findComponentFromTableCell(wait, i, "Status")
    status_text = status_component.text
    
    if status_text != "Active":
        emp_id_component = TableUtils.findComponentFromTableCell(wait, i, "Employee ID")
        inactive_employees.append(emp_id_component.text)

print(f"Inactive employees: {inactive_employees}")
```

### Bulk Actions
```python
# Select all items in a table
table = TableUtils.findTableByColumnName(wait, "Select")
row_count = TableUtils.rowCount(table)

for i in range(row_count):
    checkbox = TableUtils.findComponentFromTableCell(wait, i, "Select")
    if not checkbox.is_selected():
        checkbox.click()

# Perform bulk action
ButtonUtils.clickByLabelText(wait, "Delete Selected")
```

### Data Extraction
```python
# Extract employee data from table
table = TableUtils.findTableByColumnName(wait, "Employee ID")
row_count = TableUtils.rowCount(table)

employees = []
for i in range(row_count):
    emp_data = {
        'id': TableUtils.findComponentFromTableCell(wait, i, "Employee ID").text,
        'name': TableUtils.findComponentFromTableCell(wait, i, "Name").text,
        'department': TableUtils.findComponentFromTableCell(wait, i, "Department").text,
        'status': TableUtils.findComponentFromTableCell(wait, i, "Status").text
    }
    employees.append(emp_data)

print(f"Extracted {len(employees)} employee records")
```

### Table Search and Filter
```python
def find_employee_by_id(wait, employee_id):
    """Find a specific employee by ID in the table"""
    table = TableUtils.findTableByColumnName(wait, "Employee ID")
    row_count = TableUtils.rowCount(table)
    
    for i in range(row_count):
        id_component = TableUtils.findComponentFromTableCell(wait, i, "Employee ID")
        if id_component.text == employee_id:
            return {
                'row_index': i,
                'name': TableUtils.findComponentFromTableCell(wait, i, "Name").text,
                'status': TableUtils.findComponentFromTableCell(wait, i, "Status").text
            }
    
    return None

# Usage
employee = find_employee_by_id(wait, "EMP001")
if employee:
    print(f"Found employee: {employee['name']} at row {employee['row_index']}")
```

### Row-Specific Actions
```python
# Edit specific employee record
def edit_employee_status(wait, employee_id, new_status):
    table = TableUtils.findTableByColumnName(wait, "Employee ID")
    row_count = TableUtils.rowCount(table)
    
    for i in range(row_count):
        id_component = TableUtils.findComponentFromTableCell(wait, i, "Employee ID")
        if id_component.text == employee_id:
            # Click edit button for this row
            edit_button = TableUtils.findComponentFromTableCell(wait, i, "Actions")
            edit_button.click()
            
            # Update status
            DropdownUtils.selectDropdownValueByLabelText(wait, "Status", new_status)
            ButtonUtils.clickByLabelText(wait, "Save")
            return True
    
    return False

# Edit employee EMP001 status to Inactive
edit_employee_status(wait, "EMP001", "Inactive")
```

## Technical Details

### Table Structure

TableUtils expects Appian tables with this structure:
```html
<table>
  <thead>
    <tr>
      <th scope="col" abbr="Employee ID" class="headCell_0">Employee ID</th>
      <th scope="col" abbr="Name" class="headCell_1">Name</th>
      <th scope="col" abbr="Status" class="headCell_2">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr data-dnd-name="row 1">
      <td>EMP001</td>
      <td>John Doe</td>
      <td>Active</td>
    </tr>
  </tbody>
</table>
```

1. Finds the header cell with matching `abbr` attribute
2. Extracts the column number from the `headCell_X` CSS class
3. Returns the 0-based column index

### Row Selection Logic

The XPath for row selection:
```xpath
./tbody/tr[./td[not (@data-empty-grid-message)]]
- Header rows
- Non-data rows

### Cell Component Selection

The XPath for finding cell components:
```xpath
.//table[./thead/tr/th[@abbr="{columnName}"]]/tbody/tr[@data-dnd-name="row {rowNumber}"]/td[not (@data-empty-grid-message)][{columnNumber}]/*
```

- The component within the cell

## Troubleshooting

### Common Issues

**Solutions:**
- Verify exact column name spelling and case
- Check if table is loaded and visible
- Ensure column name matches the `abbr` attribute in table headers
- Wait for any dynamic table loading to complete

**Solutions:**
- Check if table has pagination
- Verify filters are not hiding rows
- Ensure table data is fully loaded
- Check for empty state messages

**Cell Component Not Found:**
```
RuntimeError: Could not find component in cell at row 1, column 'Status'
```
**Solutions:**
- Verify row index is within table bounds (0-based indexing)
- Check if the specified column exists
- Ensure cell contains an interactive component
- Verify table structure matches expected format

### Debugging Tips

1. **Inspect Table Structure**:
   ```python
   # Get table and inspect HTML
   table = TableUtils.findTableByColumnName(wait, "Employee ID")
   print(table.get_attribute("outerHTML"))
   ```

2. **Verify Column Names**:
   ```python
   # Find all column headers
   headers = table.find_elements(By.XPATH, ".//thead/tr/th")
   for header in headers:
       print(f"Column: {header.get_attribute('abbr')}")
   ```

3. **Check Row Structure**:
   ```python
   # Inspect specific row
   rows = table.find_elements(By.XPATH, ".//tbody/tr")
   print(f"Found {len(rows)} rows")
   for i, row in enumerate(rows):
       print(f"Row {i}: {row.get_attribute('data-dnd-name')}")
   ```

## Integration Examples

### With pytest and Data Validation
```python
import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from robo_appian.components.TableUtils import TableUtils

class TestTableData:
    def setup_method(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)
    
    def teardown_method(self):
        self.driver.quit()
    
    def test_employee_table_data(self):
        self.driver.get("https://your-appian-app.com")
        
        # Validate table exists and has data
        table = TableUtils.findTableByColumnName(self.wait, "Employee ID")
        row_count = TableUtils.rowCount(table)
        
        assert row_count > 0, "Employee table should contain data"
        
        # Validate first row data
        emp_id = TableUtils.findComponentFromTableCell(self.wait, 0, "Employee ID").text
        assert emp_id.startswith("EMP"), f"Invalid employee ID format: {emp_id}"
        
        # Check status values
        for i in range(row_count):
            status = TableUtils.findComponentFromTableCell(self.wait, i, "Status").text
            assert status in ["Active", "Inactive"], f"Invalid status: {status}"
```

### With Page Object Model
```python
class EmployeeManagementPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def get_employee_count(self):
        table = TableUtils.findTableByColumnName(self.wait, "Employee ID")
        return TableUtils.rowCount(table)
    
    def find_employee_by_id(self, emp_id):
        table = TableUtils.findTableByColumnName(self.wait, "Employee ID")
        row_count = TableUtils.rowCount(table)
        
        for i in range(row_count):
            id_component = TableUtils.findComponentFromTableCell(self.wait, i, "Employee ID")
            if id_component.text == emp_id:
                return {
                    'row': i,
                    'name': TableUtils.findComponentFromTableCell(self.wait, i, "Name").text,
                    'status': TableUtils.findComponentFromTableCell(self.wait, i, "Status").text,
                    'department': TableUtils.findComponentFromTableCell(self.wait, i, "Department").text
                }
        return None
    
    def update_employee_status(self, emp_id, new_status):
        employee = self.find_employee_by_id(emp_id)
        if employee:
            edit_button = TableUtils.findComponentFromTableCell(
                self.wait, employee['row'], "Actions"
            )
            edit_button.click()
            
            DropdownUtils.selectDropdownValueByLabelText(self.wait, "Status", new_status)
            ButtonUtils.clickByLabelText(self.wait, "Save")
            return True
        return False
```

### With Data Export Functionality
```python
import csv

class TableDataExporter:
    def __init__(self, wait):
        self.wait = wait
    
    def export_table_to_csv(self, column_name, output_file, columns):
        """Export table data to CSV file"""
        table = TableUtils.findTableByColumnName(self.wait, column_name)
        row_count = TableUtils.rowCount(table)
        
        with open(output_file, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=columns)
            writer.writeheader()
            
            for i in range(row_count):
                row_data = {}
                for col in columns:
                    try:
                        component = TableUtils.findComponentFromTableCell(self.wait, i, col)
                        row_data[col] = component.text
                    except Exception:
                        row_data[col] = ""  # Handle missing data
                
# Usage
exporter.export_table_to_csv(
    "Employee ID", 
    "employees.csv", 
    ["Employee ID", "Name", "Department", "Status", "Hire Date"]
)
```

## Related Components

- **[ButtonUtils](button-utils.md)** - For interacting with action buttons in table cells
- **[DropdownUtils](dropdown-utils.md)** - For dropdown selections in table cells
- **[InputUtils](input-utils.md)** - For input fields in editable table cells
- **[ComponentDriver](component-driver.md)** - For universal component interactions

---

*TableUtils provides powerful table interaction capabilities for Appian applications, enabling reliable data extraction, validation, and manipulation operations on complex table structures.*
