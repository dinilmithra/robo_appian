# Robo Utils

## Overview

RoboUtils provides resilience utilities for handling flaky operations. The primary feature is automatic retry logic for operations that may encounter timeout exceptions.

Use these utilities to make your tests more robust against temporary delays, network issues, or animation timing problems.

## Methods

### retry_on_timeout

Automatically retry an operation that may fail due to timeout exceptions.

Use this to wrap flaky operations like waiting for slow-loading elements, clicking buttons that trigger animations, or interacting with elements during page transitions. The method retries only on TimeoutException; other exceptions are immediately re-raised.

**Args:**

- `operation` (callable): A function or lambda that performs the desired operation (takes no arguments)
- `max_retries` (int): Maximum number of total attempts (initial + retries). Default is 3
- `operation_name` (str): Descriptive name for the operation (used in error messages). Default is "operation"

**Returns:**

- The return value from the successful execution of the operation

**Raises:**

- `TimeoutException`: If operation fails with TimeoutException for all retry attempts
- `Exception`: Any non-timeout exceptions are immediately re-raised without retry

**Examples:**

HTML:
```html
<button id="load_more" onclick="loadMoreItems()">
  Load More
</button>
<!-- JavaScript delays rendering new items -->
```

Python:
```python
from robo_appian.utils.RoboUtils import RoboUtils
from robo_appian.components.ButtonUtils import ButtonUtils

# Wrap a flaky button click operation
def click_load_more():
    ButtonUtils.clickByLabelText(wait, "Load More")

# Retry up to 3 times if timeout occurs
RoboUtils.retry_on_timeout(
    click_load_more, 
    max_retries=3, 
    operation_name="Load More Click"
)
```

**Advanced Example - Retrying Complex Operations:**

```python
from robo_appian.utils.RoboUtils import RoboUtils
from robo_appian.components import InputUtils, DropdownUtils, ButtonUtils

def submit_form():
    """Multi-step form submission that might timeout"""
    InputUtils.setValueByLabelText(wait, "Title", "Test Request")
    DropdownUtils.selectDropdownValueByLabelText(wait, "Priority", "High")
    ButtonUtils.clickByLabelText(wait, "Submit")

# Retry entire form submission up to 5 times
RoboUtils.retry_on_timeout(
    submit_form,
    max_retries=5,
    operation_name="Form Submission"
)
```

**Using with Lambda Functions:**

```python
from robo_appian.utils.RoboUtils import RoboUtils
from robo_appian.components.LabelUtils import LabelUtils

# Retry checking for a success message
result = RoboUtils.retry_on_timeout(
    lambda: LabelUtils.isLabelExists(wait, "Successfully Saved"),
    max_retries=3,
    operation_name="Check Success Message"
)
```

**Handling Return Values:**

```python
from robo_appian.utils.RoboUtils import RoboUtils
from robo_appian.components.TableUtils import TableUtils

# Retry getting table row count
def get_row_count():
    table = TableUtils.findTableByColumnName(wait, "Employee ID")
    return TableUtils.rowCount(table)

row_count = RoboUtils.retry_on_timeout(
    get_row_count,
    max_retries=3,
    operation_name="Get Table Rows"
)
print(f"Table has {row_count} rows")
```

## Best Practices

### When to Use Retry Logic

**Good Use Cases:**
- Elements that load after animations or transitions
- Operations affected by network latency
- Click actions on elements that trigger async operations
- Waiting for dynamically generated content

**Avoid Overuse:**
- Don't mask real failures - if an operation consistently times out, fix the root cause
- Avoid high retry counts (3-5 is usually sufficient)
- Don't use for operations that should fail fast (authentication, validation errors)

### Logging and Debugging

RoboUtils uses Python's logging module. Configure logging in your test setup to see retry attempts:

```python
import logging

# Configure logging to see retry messages
logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Now retry messages will be logged
from robo_appian.utils.RoboUtils import RoboUtils

RoboUtils.retry_on_timeout(
    lambda: ButtonUtils.clickByLabelText(wait, "Submit"),
    max_retries=3,
    operation_name="Submit Button"
)
```

### Combining with Other Utilities

```python
from robo_appian.utils.RoboUtils import RoboUtils
from robo_appian.components import SearchDropdownUtils, DateUtils, ButtonUtils

def fill_and_submit_form():
    """Complex form interaction with multiple components"""
    # Search dropdown can be slow
    SearchDropdownUtils.selectSearchDropdownValueByLabelText(
        wait, 
        "Approver", 
        "John Smith"
    )
    
    # Date picker interaction
    DateUtils.setValueByLabelText(wait, "Due Date", "12/31/2025")
    
    # Submit button
    ButtonUtils.clickByLabelText(wait, "Submit")

# Retry the entire sequence
RoboUtils.retry_on_timeout(
    fill_and_submit_form,
    max_retries=3,
    operation_name="Fill and Submit Form"
)
```