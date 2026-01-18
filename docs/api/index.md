# API Reference

Complete reference for all robo_appian utilities and components. All methods follow the **wait-first pattern**: pass `WebDriverWait` as the first argument.

## Component Utilities

Located under `robo_appian.components`, these utilities handle interaction with specific Appian UI elements:

- **[Buttons](button-utils.md)** - Click buttons and action links by label
- **[Inputs](input-utils.md)** - Fill text inputs by label or placeholder
- **[Dates](date-utils.md)** - Set date values in date pickers
- **[Dropdowns](dropdown-utils.md)** - Select from standard dropdowns
- **[Search Dropdowns](search-dropdown-utils.md)** - Select from filterable dropdowns
- **[Search Inputs](search-input-utils.md)** - Interact with searchable input fields
- **[Tables](table-utils.md)** - Find rows, click cells, read table data
- **[Tabs](tab-utils.md)** - Switch between tab panels
- **[Links](link-utils.md)** - Click links by visible text
- **[Labels](label-utils.md)** - Find and verify label text

## Shared Utilities

Located under `robo_appian.utils`, these provide low-level helpers:

- **[ComponentUtils](component-utils.md)** - Element waiting, safe clicking, XPath queries
- **[RoboUtils](robo-utils.md)** - Retry logic, resilience helpers
- **[BrowserUtils](browser-utils.md)** - Multi-tab/window management

## Quick Examples

### Set form values
```python
from robo_appian.components import InputUtils, DateUtils, DropdownUtils

InputUtils.setValueByLabelText(wait, "Name", "John Doe")
DateUtils.setValueByLabelText(wait, "Start Date", "01/15/2025")
DropdownUtils.selectDropdownValueByLabelText(wait, "Status", "Active")
```

### Interact with tables
```python
from robo_appian.components import TableUtils, ButtonUtils

table = TableUtils.findTableByColumnName(wait, "ID")
TableUtils.selectRowFromTableByColumnNameAndRowNumber(wait, 0, "ID")
button = TableUtils.findComponentFromTableCell(wait, 0, "Actions")
ButtonUtils.clickByLabelText(wait, "Edit")
```

### Handle retries
```python
from robo_appian.utils.RoboUtils import RoboUtils
from robo_appian.components import ButtonUtils

RoboUtils.retry_on_timeout(
    lambda: ButtonUtils.clickByLabelText(wait, "Submit"),
    max_retries=3,
    operation_name="click submit"
)
```

See the [Components guide](../user-guide/components.md) for detailed usage patterns and best practices.
