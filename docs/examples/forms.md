# Form Automation

Fill and submit a typical Appian form with text, dropdown, date, and search controls.

## Basic Form Fill

```python
from robo_appian.components import InputUtils, DropdownUtils, DateUtils, SearchDropdownUtils, ButtonUtils

# Text fields
InputUtils.setValueByLabelText(wait, "First Name", "Ada")
InputUtils.setValueByLabelText(wait, "Last Name", "Lovelace")
InputUtils.setValueByPlaceholderText(wait, "Enter email", "ada@example.com")

# Dropdowns
DropdownUtils.selectDropdownValueByLabelText(wait, "Status", "Active")
DropdownUtils.selectDropdownValueByPartialLabelText(wait, "Country", "United States")

# Date picker
DateUtils.setValueByLabelText(wait, "Start Date", "01/01/2025")

# Search dropdown
SearchDropdownUtils.selectSearchDropdownValueByLabelText(wait, "Manager", "Grace Hopper")

# Submit
ButtonUtils.clickByLabelText(wait, "Submit")
```

## Multi-Step Form with Validation

```python
from robo_appian.components import InputUtils, LabelUtils, ButtonUtils

# Fill first section
InputUtils.setValueByLabelText(wait, "Project Name", "Migration Project")
InputUtils.setValueByLabelText(wait, "Budget", "50000")

# Click Next
ButtonUtils.clickByLabelText(wait, "Next")

# Verify moved to next step
LabelUtils.isLabelExists(wait, "Step 2: Team Assignment")

# Fill second section
SearchInputUtils.selectSearchDropdownByLabelText(wait, "Project Lead", "John Smith")
DropdownUtils.selectDropdownValueByLabelText(wait, "Department", "Engineering")

# Submit final form
ButtonUtils.clickByLabelText(wait, "Submit")
```

## Conditional Form Fields

```python
from robo_appian.components import DropdownUtils, InputUtils, LabelUtils

# Select option that reveals additional fields
DropdownUtils.selectDropdownValueByLabelText(wait, "Request Type", "New Equipment")

# Wait for conditional field to appear
LabelUtils.isLabelExists(wait, "Equipment Details")

# Fill conditional fields
InputUtils.setValueByLabelText(wait, "Equipment Type", "Laptop")
InputUtils.setValueByLabelText(wait, "Justification", "Current device is 5 years old")
```

## Form with Multiple Date Fields

```python
from robo_appian.components import DateUtils, ComponentUtils

# Set multiple dates
DateUtils.setValueByLabelText(wait, "Start Date", "01/15/2025")
DateUtils.setValueByLabelText(wait, "End Date", "03/31/2025")
DateUtils.setValueByLabelText(wait, "Review Date", "02/15/2025")

# Use utility functions for dynamic dates
today = ComponentUtils.today()
yesterday = ComponentUtils.yesterday()

DateUtils.setValueByLabelText(wait, "Submission Date", today)
DateUtils.setValueByLabelText(wait, "Last Modified", yesterday)
```

## Search Input with Auto-Complete

```python
from robo_appian.components import SearchInputUtils

# Type and select from search input (not dropdown)
SearchInputUtils.selectSearchDropdownByLabelText(wait, "Employee", "Alice Johnson")

# Use partial matching for large result sets
SearchInputUtils.selectSearchDropdownByPartialLabelText(wait, "Department", "Engineer")
```

## Handling Read-Only Fields

```python
from robo_appian.components import DropdownUtils, InputUtils, LabelUtils

# Verify field is read-only before attempting to edit
is_readonly = DropdownUtils.checkReadOnlyStatusByLabelText(wait, "Approval Status")

if not is_readonly:
    DropdownUtils.selectDropdownValueByLabelText(wait, "Approval Status", "Approved")
else:
    # Log or handle read-only state
    print("Approval Status is read-only")
```

Notes:
- Labels must have `for` attributes for inputs/dates. If missing, create a targeted XPath and reuse `ComponentUtils` helpers.
- Dropdown locators rely on `aria-controls`; if custom widgets differ, inspect DOM to align the pattern.
- Use `LabelUtils.isLabelExists()` to verify section headers or conditional fields before interacting.
