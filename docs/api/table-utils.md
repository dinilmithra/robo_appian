# Table Utils

## Overview

TableUtils provides methods to interact with Appian grid and table components. Use TableUtils to read cells, click rows, find elements within table cells, and query tables using column names and row indices. Tables are located by their column headers, and rows are accessed using 0-based indexing in public APIs (internally converted to 1-based for Appian's DOM structure).

## Methods

### findTableByColumnName

Find a table element by any of its column names.

Use this when you need to locate a table component and you know one of its column header names. Returns the table WebElement for further operations like counting rows or extracting data. Essential for identifying the correct table when multiple tables exist on the page.

**Args:**

- `wait` (WebDriverWait): WebDriverWait instance with configured timeout
- `column_name` (str): Exact column header text (from the abbr attribute)

**Raises:**

- `TimeoutException`: If table with specified column not found within timeout

**Returns:** WebElement representing the table

**Examples:**

HTML:
```html
<table>
  <thead>
    <tr>
      <th abbr="Employee ID" scope="col">Employee ID</th>
      <th abbr="Name" scope="col">Name</th>
      <th abbr="Status" scope="col">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr data-dnd-name="row 1">
      <td>001</td>
      <td>John Doe</td>
      <td>Active</td>
    </tr>
  </tbody>
</table>
```

Python:
```python
from robo_appian.components.TableUtils import TableUtils
from selenium.webdriver.support.ui import WebDriverWait

table = TableUtils.findTableByColumnName(wait, "Employee ID")
```

---

### rowCount

Count the number of data rows in a table.

Use this to verify table content, validate search results, or determine if a table has data before processing rows. Excludes empty grid message rows, returning only actual data rows. Returns 0 if the table is empty.

**Args:**

- `table` (WebElement): Table element (obtained from findTableByColumnName)

**Raises:** None

**Returns:** int: Number of data rows in the table

**Examples:**

HTML:
```html
<table>
  <tbody>
    <tr data-dnd-name="row 1"><td>Data 1</td></tr>
    <tr data-dnd-name="row 2"><td>Data 2</td></tr>
    <tr data-dnd-name="row 3"><td>Data 3</td></tr>
  </tbody>
</table>
```

Python:
```python
from robo_appian.components.TableUtils import TableUtils
from selenium.webdriver.support.ui import WebDriverWait

table = TableUtils.findTableByColumnName(wait, "Name")
count = TableUtils.rowCount(table)
print(f"Table has {count} rows")
assert count > 0, "Table should have data"
```

---

### selectRowFromTableByColumnNameAndRowNumber

Click a table row to select it or trigger row actions.

Use this to select a row by clicking anywhere on it, typically to highlight the row or trigger navigation to a detail page. Row numbers are 0-based (first row is 0). Useful when clicking a row performs an action like opening a form or showing details.

**Args:**

- `wait` (WebDriverWait): WebDriverWait instance with configured timeout
- `row_number` (int): 0-based row index (first row = 0)
- `column_name` (str): Any column name in the table (used to locate the table)

**Raises:**

- `TimeoutException`: If table or row not found or not clickable within timeout

**Returns:** None

**Examples:**

HTML:
```html
<table>
  <thead>
    <tr><th abbr="Name" scope="col">Name</th></tr>
  </thead>
  <tbody>
    <tr data-dnd-name="row 1"><td>John Doe</td></tr>
    <tr data-dnd-name="row 2"><td>Jane Smith</td></tr>
  </tbody>
</table>
```

Python:
```python
from robo_appian.components.TableUtils import TableUtils
from selenium.webdriver.support.ui import WebDriverWait

TableUtils.selectRowFromTableByColumnNameAndRowNumber(wait, 0, "Name")
```

---

### findComponentFromTableCell

Find an interactive element inside a specific table cell.

Use this when you need to interact with buttons, links, inputs, or other components within a table cell. Locates the cell by row number (0-based) and column name, then returns the first interactive component inside that cell. Essential for clicking action buttons in table rows.

**Args:**

- `wait` (WebDriverWait): WebDriverWait instance with configured timeout
- `row_number` (int): 0-based row index (first row = 0)
- `column_name` (str): Exact column name where the component is located

**Raises:**

- `TimeoutException`: If table, row, or component not found or not clickable within timeout

**Returns:** WebElement representing the component in the cell

**Examples:**

HTML:
```html
<table>
  <thead>
    <tr>
      <th abbr="Name" scope="col">Name</th>
      <th abbr="Actions" scope="col">Actions</th>
    </tr>
  </thead>
  <tbody>
    <tr data-dnd-name="row 1">
      <td>John Doe</td>
      <td><button>Edit</button></td>
    </tr>
  </tbody>
</table>
```

Python:
```python
from robo_appian.components.TableUtils import TableUtils
from selenium.webdriver.support.ui import WebDriverWait

edit_button = TableUtils.findComponentFromTableCell(wait, 0, "Actions")
edit_button.click()
```

---

### findComponentByColumnNameAndRowNumber

Find an interactive element in a table cell using column and row coordinates.

Use this as an alternative to findComponentFromTableCell when you need more control over element discovery. This method uses a different internal lookup strategy that may work better with certain table structures. Returns the clickable component at the specified cell location.

**Args:**

- `wait` (WebDriverWait): WebDriverWait instance with configured timeout
- `row_number` (int): 0-based row index (first row = 0)
- `column_name` (str): Exact column name (from abbr attribute)

**Raises:**

- `TimeoutException`: If table, row, column, or component not found within timeout

**Returns:** WebElement representing the component in the cell

**Examples:**

HTML:
```html
<table>
  <thead>
    <tr>
      <th abbr="Employee ID" id="col_0" scope="col">ID</th>
      <th abbr="Status" id="col_1" scope="col">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr data-dnd-name="row 1">
      <td>001</td>
      <td><span class="status-badge">Active</span></td>
    </tr>
  </tbody>
</table>
```

Python:
```python
from robo_appian.components.TableUtils import TableUtils
from selenium.webdriver.support.ui import WebDriverWait

status_badge = TableUtils.findComponentByColumnNameAndRowNumber(wait, 0, "Status")
print(f"Status: {status_badge.text}")
```