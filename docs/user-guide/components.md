# Core Components

This guide highlights how each `*Utils` class locates and interacts with Appian components. All methods accept `wait: WebDriverWait` first.

## Inputs
- **Exact label**: `InputUtils.setValueByLabelText(wait, "Username", "alice")`
- **Partial label**: `InputUtils.setValueByPartialLabelText(wait, "User", "alice")`
- **By placeholder**: `InputUtils.setValueByPlaceholderText(wait, "Enter email", "alice@example.com")`
- Behavior: waits for clickability, moves to element, clears, then types. Labels must have a `for` attribute pointing to the input.

## Buttons
- **Exact label**: `ButtonUtils.clickByLabelText(wait, "Submit")`
- **Partial label**: `ButtonUtils.clickByPartialLabelText(wait, "Save")`
- **By id**: `ButtonUtils.clickById(wait, "save_btn")`
- Behavior: waits for `element_to_be_clickable`, uses `ComponentUtils.click` (ActionChains) to handle overlays.

## Dropdowns
- **Select**: `DropdownUtils.selectDropdownValueByLabelText(wait, "Status", "Active")`
- **Partial label**: `selectDropdownValueByPartialLabelText(...)`
- **Checks**: `checkEditableStatusByLabelText`, `checkReadOnlyStatusByLabelText`, `waitForDropdownToBeEnabled`
- Locators: label ➜ nearest combobox (`role="combobox"`), uses `aria-controls` to find the option list.

## Search Dropdowns
- **Select**: `SearchDropdownUtils.selectSearchDropdownValueByLabelText(wait, "Employee", "John Doe")`
- Pattern: combobox ID with `_value` suffix ➜ search input `*_searchInput` ➜ options list `*_list`.

## Search Inputs
- **Select**: `SearchInputUtils.selectSearchDropdownByLabelText(wait, "City", "Boston")`
- Pattern: label ➜ `_searchInput` input ➜ `_list` options.

## Dates
- **Set**: `DateUtils.setValueByLabelText(wait, "Start Date", "01/01/2025")`
- Clears and types the date string; relies on label `for` attribute.

## Tabs, Links, Labels
- **Tabs**: `TabUtils.selectTabByLabelText(wait, "Details")`
- **Links**: `LinkUtils.click(wait, "View more")`
- **Labels**: `LabelUtils.isLabelExists(wait, "Important notice")`

## Tables
- **Find table**: `TableUtils.findTableByColumnName(wait, "Employee ID")`
- **Click row by column + index**: `TableUtils.selectRowFromTableByColumnNameAndRowNumber(wait, 0, "Employee ID")`
- **Find cell component**: `TableUtils.findComponentFromTableCell(wait, 1, "Status")`
- Column resolution uses header `abbr` plus header class/id parsing. Public APIs use 0-based `rowNumber`; internally converted to Appian's 1-based rows.

For detailed signatures and parameters, see the [API Reference](../api/index.md).
