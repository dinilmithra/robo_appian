# Complex Workflows

Drive multi-step flows using component utilities for clear, maintainable test code.

## Approval Workflow

```python
from robo_appian.components import TableUtils, ButtonUtils, InputUtils, LabelUtils

# Navigate to pending approvals
ButtonUtils.clickByLabelText(wait, "My Approvals")

# Find table of pending requests
table = TableUtils.findTableByColumnName(wait, "Request ID")
row_count = TableUtils.rowCount(table)

# Approve specific request
for row_index in range(row_count):
    request_cell = TableUtils.findComponentByColumnNameAndRowNumber(wait, row_index, "Request Title")
    
    if "Laptop" in request_cell.text:
        # Click review button
        TableUtils.selectRowFromTableByColumnNameAndRowNumber(wait, row_index, "Request ID")
        
        # Add approval comments
        InputUtils.setValueByLabelText(wait, "Comments", "Approved for Q1 budget")
        
        # Approve
        ButtonUtils.clickByLabelText(wait, "Approve")
        break
```

## Multi-Page Workflow with Validation

```python
from robo_appian.components import InputUtils, DropdownUtils, DateUtils, ButtonUtils, LabelUtils

# Page 1: Basic Information
InputUtils.setValueByLabelText(wait, "Project Name", "Cloud Migration")
DropdownUtils.selectDropdownValueByLabelText(wait, "Project Type", "Infrastructure")
DateUtils.setValueByLabelText(wait, "Start Date", "03/01/2025")

ButtonUtils.clickByLabelText(wait, "Next")

# Verify page 2 loaded
LabelUtils.isLabelExists(wait, "Budget Details")

# Page 2: Budget
InputUtils.setValueByLabelText(wait, "Estimated Cost", "150000")
DropdownUtils.selectDropdownValueByLabelText(wait, "Cost Center", "IT-Operations")

ButtonUtils.clickByLabelText(wait, "Next")

# Verify page 3 loaded
LabelUtils.isLabelExists(wait, "Team Assignment")

# Page 3: Team
SearchDropdownUtils.selectSearchDropdownValueByLabelText(wait, "Project Manager", "Alice Brown")
SearchDropdownUtils.selectSearchDropdownValueByLabelText(wait, "Technical Lead", "Bob Wilson")

# Review and Submit
ButtonUtils.clickByLabelText(wait, "Review")
LabelUtils.isLabelExists(wait, "Confirmation")
ButtonUtils.clickByLabelText(wait, "Submit")
```

## Conditional Workflow Paths

```python
from robo_appian.components import DropdownUtils, InputUtils, ButtonUtils, LabelUtils

# Select request type
DropdownUtils.selectDropdownValueByLabelText(wait, "Request Type", "Equipment")

# Path diverges based on selection
try:
    # Check if equipment-specific fields appear
    LabelUtils.isLabelExists(wait, "Equipment Details")
    
    # Fill equipment-specific form
    InputUtils.setValueByLabelText(wait, "Item Description", "MacBook Pro")
    InputUtils.setValueByLabelText(wait, "Quantity", "1")
    DropdownUtils.selectDropdownValueByLabelText(wait, "Urgency", "Standard")
    
except:
    # Different path for other request types
    InputUtils.setValueByLabelText(wait, "Description", "General request")

# Common final step
ButtonUtils.clickByLabelText(wait, "Submit")
```

## Retry Workflow with Error Handling

```python
from robo_appian.utils.RoboUtils import RoboUtils
from robo_appian.components import ButtonUtils, InputUtils, LabelUtils

def submit_form():
    """Submit form with retry logic"""
    InputUtils.setValueByLabelText(wait, "Title", "Test Request")
    ButtonUtils.clickByLabelText(wait, "Submit")
    
    # Verify success
    LabelUtils.isLabelExists(wait, "Request Submitted Successfully")

# Retry up to 3 times on timeout
RoboUtils.retry_on_timeout(submit_form, max_retries=3, name="Submit Form")
```

## Complete End-to-End Workflow

```python
from robo_appian.controllers.ComponentDriver import ComponentDriver
from robo_appian.components import TableUtils, ButtonUtils, LabelUtils, InputUtils, DropdownUtils, SearchDropdownUtils

# Step 1: Create new request
ButtonUtils.clickByLabelText(wait, "New Request")

# Fill request form using component utilities
InputUtils.setValueByLabelText(wait, "Request Title", "Software License")
InputUtils.setValueByLabelText(wait, "Justification", "Required for project")
DropdownUtils.selectDropdownValueByLabelText(wait, "Category", "Software")
SearchDropdownUtils.selectSearchDropdownValueByLabelText(wait, "Approver", "Manager Name")
ButtonUtils.clickByLabelText(wait, "Submit")

# Step 2: Verify request appears in tracking
LabelUtils.isLabelExists(wait, "Request Submitted")
ButtonUtils.clickByLabelText(wait, "View My Requests")

# Step 3: Find submitted request in table
table = TableUtils.findTableByColumnName(wait, "Title")
row_count = TableUtils.rowCount(table)

request_found = False
for row_index in range(row_count):
    title_cell = TableUtils.findComponentByColumnNameAndRowNumber(wait, row_index, "Title")
    
    if title_cell.text == "Software License":
        # Verify status
        status_cell = TableUtils.findComponentByColumnNameAndRowNumber(wait, row_index, "Status")
        assert status_cell.text == "Pending", f"Expected Pending but got {status_cell.text}"
        request_found = True
        break

assert request_found, "Submitted request not found in tracking table"
```

## Tab Navigation Workflow

```python
from robo_appian.components import TabUtils, TableUtils, ButtonUtils

# Navigate to different workflow stages using tabs
TabUtils.selectTabByLabelText(wait, "Active Requests")

# Process active requests
table = TableUtils.findTableByColumnName(wait, "Request ID")
row_count = TableUtils.rowCount(table)
print(f"Active requests: {row_count}")

# Switch to completed tab
TabUtils.selectTabByLabelText(wait, "Completed")

# Verify tab is active
is_selected = TabUtils.checkTabSelectedByLabelText(wait, "Completed")
assert is_selected, "Completed tab not selected"

# Process completed requests
table = TableUtils.findTableByColumnName(wait, "Request ID")
completed_count = TableUtils.rowCount(table)
print(f"Completed requests: {completed_count}")
```

Tips:
- Use specific component utilities for clear, readable test code.
- Wrap long flows with `RoboUtils.retry_on_timeout` for known flaky spots instead of raising global timeouts.
- Use `LabelUtils.isLabelExists()` to verify each page/step loaded before proceeding.
- For debugging, add print statements or logging between major workflow steps.
