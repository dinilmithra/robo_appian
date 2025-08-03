# Core Components

This guide provides detailed documentation for all Robo Appian core components. Each component is designed to handle specific types of UI elements in Appian applications.

## Component Overview

Robo Appian provides specialized utilities for different types of UI components:

| Component | Purpose | Primary Use Cases |
|-----------|---------|------------------|
| **ButtonUtils** | Button interactions | Clicking buttons, form submissions |
| **InputUtils** | Text input handling | Entering text, clearing fields |
| **DropdownUtils** | Dropdown operations | Selecting options, managing comboboxes |
| **DateUtils** | Date picker handling | Setting dates, date validations |
| **TableUtils** | Table operations | Data extraction, row counting |
| **TabUtils** | Tab navigation | Switching between tabs |
| **LabelUtils** | Label text operations | Reading text values |
| **LinkUtils** | Link interactions | Clicking links, navigation |

## ButtonUtils

Handles all button-related interactions in Appian applications.

### Key Methods

```python
from robo_appian.components.ButtonUtils import ButtonUtils

# Click button by label text
ButtonUtils.clickByLabelText(wait, "Submit")
ButtonUtils.clickByLabelText(wait, "Save Changes")
ButtonUtils.clickByLabelText(wait, "Cancel")
```

### Usage Examples

```python
def test_form_submission():
    """Example of button interactions in a form"""
    # Fill form fields first...
    
    # Save as draft
    ButtonUtils.clickByLabelText(wait, "Save as Draft")
    
    # Verify draft saved, then submit
    if ComponentUtils.checkComponentExistsByXpath(wait, "//div[contains(text(), 'Draft saved')]"):
        ButtonUtils.clickByLabelText(wait, "Submit for Approval")
    
    # Handle confirmation dialog
    ButtonUtils.clickByLabelText(wait, "Confirm")
```

### Best Practices

- Use exact button text as it appears to users
- Handle confirmation dialogs separately
- Wait for page changes before next actions

## InputUtils

Manages text input fields including single-line inputs, text areas, and search fields.

### Key Methods

```python
from robo_appian.components.InputUtils import InputUtils

# Set value by label text
InputUtils.setValueByLabelText(wait, "First Name", "John")

# Set value by component ID
InputUtils.setValueById(wait, "employee-id", "EMP001")
```

### Usage Examples

```python
def fill_employee_form():
    """Complete employee form example"""
    # Personal information
    InputUtils.setValueByLabelText(wait, "Employee ID", "EMP2024001")
    InputUtils.setValueByLabelText(wait, "First Name", "John")
    InputUtils.setValueByLabelText(wait, "Last Name", "Doe")
    InputUtils.setValueByLabelText(wait, "Email", "john.doe@company.com")
    
    # Address information
    InputUtils.setValueByLabelText(wait, "Street Address", "123 Main St")
    InputUtils.setValueByLabelText(wait, "City", "San Francisco")
    InputUtils.setValueByLabelText(wait, "ZIP Code", "94102")
    
    # Additional notes (text area)
    InputUtils.setValueByLabelText(wait, "Comments", "New employee in engineering department")
```

### Advanced Techniques

```python
# Clear existing content first
def set_value_with_clear(wait, label, value):
    """Clear field before setting new value"""
    try:
        element = ComponentUtils.findComponentUsingXpath(wait, f"//input[@aria-label='{label}']")
        element.clear()
        InputUtils.setValueByLabelText(wait, label, value)
    except:
        # Fallback to regular method
        InputUtils.setValueByLabelText(wait, label, value)

# Handle autocomplete fields
def set_autocomplete_field(wait, label, value):
    """Handle fields with autocomplete/suggestions"""
    InputUtils.setValueByLabelText(wait, label, value)
    # Wait for suggestions to appear and select first one
    time.sleep(1)
    ComponentUtils.tab(wait)  # Tab to confirm selection
```

## DropdownUtils

Handles dropdown menus, comboboxes, and select lists in Appian applications.

### Key Methods

```python
from robo_appian.components.DropdownUtils import DropdownUtils

# Select by exact label and value
DropdownUtils.selectDropdownValueByLabelText(wait, "Department", "Engineering")

# Select by partial label match
DropdownUtils.selectDropdownValueByPartialLabelText(wait, "Status", "Active")
```

### Usage Examples

```python
def configure_employee_details():
    """Example of dropdown selections"""
    # Department selection
    DropdownUtils.selectDropdownValueByLabelText(wait, "Department", "Engineering")
    
    # Employment type
    DropdownUtils.selectDropdownValueByLabelText(wait, "Employment Type", "Full-time")
    
    # Status
    DropdownUtils.selectDropdownValueByLabelText(wait, "Status", "Active")
    
    # Location (using partial match for long labels)
    DropdownUtils.selectDropdownValueByPartialLabelText(wait, "Office Location", "San Francisco")
```

### Handling Complex Dropdowns

```python
def handle_dependent_dropdowns():
    """Handle dropdowns that depend on other selections"""
    # Select country first
    DropdownUtils.selectDropdownValueByLabelText(wait, "Country", "United States")
    
    # Wait for state dropdown to populate
    time.sleep(2)
    
    # Select state
    DropdownUtils.selectDropdownValueByLabelText(wait, "State", "California")
    
    # Wait for city dropdown to populate
    time.sleep(2)
    
    # Select city
    DropdownUtils.selectDropdownValueByLabelText(wait, "City", "San Francisco")
```

## DateUtils

Specialized component for handling date picker elements in Appian.

### Key Methods

```python
from robo_appian.components.DateUtils import DateUtils
from robo_appian.utils.ComponentUtils import ComponentUtils

# Set specific date
DateUtils.setValueByLabelText(wait, "Start Date", "01/15/2024")

# Use utility functions for common dates
DateUtils.setValueByLabelText(wait, "Application Date", ComponentUtils.today())
DateUtils.setValueByLabelText(wait, "Previous Date", ComponentUtils.yesterday())
```

### Usage Examples

```python
def set_project_dates():
    """Example of date field management"""
    # Project start date (today)
    DateUtils.setValueByLabelText(wait, "Project Start Date", ComponentUtils.today())
    
    # Project end date (specific date)
    DateUtils.setValueByLabelText(wait, "Project End Date", "12/31/2024")
    
    # Milestone dates
    DateUtils.setValueByLabelText(wait, "Phase 1 Completion", "03/15/2024")
    DateUtils.setValueByLabelText(wait, "Phase 2 Completion", "06/15/2024")
    DateUtils.setValueByLabelText(wait, "Final Delivery", "09/15/2024")
```

### Date Format Handling

```python
from datetime import datetime, timedelta

def calculate_and_set_dates():
    """Calculate dates based on business logic"""
    # Start date is today
    start_date = datetime.now()
    DateUtils.setValueByLabelText(wait, "Start Date", start_date.strftime("%m/%d/%Y"))
    
    # End date is 30 days from start
    end_date = start_date + timedelta(days=30)
    DateUtils.setValueByLabelText(wait, "End Date", end_date.strftime("%m/%d/%Y"))
    
    # Review date is 7 days before end
    review_date = end_date - timedelta(days=7)
    DateUtils.setValueByLabelText(wait, "Review Date", review_date.strftime("%m/%d/%Y"))
```

## TableUtils

Provides comprehensive functionality for working with data tables and grids.

### Key Methods

```python
from robo_appian.components.TableUtils import TableUtils

# Find table by column name
table = TableUtils.findTableByColumnName(wait, "Employee ID")

# Get row count
row_count = TableUtils.rowCount(table)

# Get data from specific cell
cell_data = TableUtils.findComponentFromTableCell(wait, 1, "Name").text
```

### Usage Examples

```python
def extract_employee_data():
    """Extract all employee data from table"""
    # Find the employee table
    table = TableUtils.findTableByColumnName(wait, "Employee ID")
    total_rows = TableUtils.rowCount(table)
    
    employees = []
    
    # Extract data from each row
    for row in range(1, total_rows + 1):
        try:
            employee = {
                'id': TableUtils.findComponentFromTableCell(wait, row, "Employee ID").text,
                'name': TableUtils.findComponentFromTableCell(wait, row, "Name").text,
                'department': TableUtils.findComponentFromTableCell(wait, row, "Department").text,
                'status': TableUtils.findComponentFromTableCell(wait, row, "Status").text,
                'start_date': TableUtils.findComponentFromTableCell(wait, row, "Start Date").text
            }
            employees.append(employee)
            
        except Exception as e:
            print(f"Error processing row {row}: {e}")
            continue
    
    return employees

def validate_employee_in_table(expected_employee):
    """Validate specific employee appears in table"""
    table = TableUtils.findTableByColumnName(wait, "Employee ID")
    total_rows = TableUtils.rowCount(table)
    
    for row in range(1, total_rows + 1):
        emp_id = TableUtils.findComponentFromTableCell(wait, row, "Employee ID").text
        if emp_id == expected_employee['id']:
            # Found the employee, validate details
            name = TableUtils.findComponentFromTableCell(wait, row, "Name").text
            department = TableUtils.findComponentFromTableCell(wait, row, "Department").text
            
            assert name == expected_employee['name'], f"Name mismatch: {name} != {expected_employee['name']}"
            assert department == expected_employee['department'], f"Department mismatch: {department} != {expected_employee['department']}"
            
            return True
    
    raise AssertionError(f"Employee {expected_employee['id']} not found in table")
```

### Table Interactions

```python
def interact_with_table_rows():
    """Example of interacting with table elements"""
    table = TableUtils.findTableByColumnName(wait, "Employee ID")
    total_rows = TableUtils.rowCount(table)
    
    for row in range(1, total_rows + 1):
        status = TableUtils.findComponentFromTableCell(wait, row, "Status").text
        
        if status == "Pending":
            # Click action button for pending employees
            action_cell = TableUtils.findComponentFromTableCell(wait, row, "Actions")
            edit_button = action_cell.find_element(By.XPATH, ".//button[contains(text(), 'Edit')]")
            edit_button.click()
            
            # Perform some action, then continue
            break
```

## TabUtils

Handles tab navigation within Appian interfaces.

### Key Methods

```python
from robo_appian.components.TabUtils import TabUtils

# Click on tab by label
TabUtils.clickTabByLabelText(wait, "General Information")
TabUtils.clickTabByLabelText(wait, "Contact Details")
TabUtils.clickTabByLabelText(wait, "Employment History")
```

### Usage Examples

```python
def complete_multi_tab_form():
    """Fill out form across multiple tabs"""
    
    # Tab 1: Personal Information
    TabUtils.clickTabByLabelText(wait, "Personal Information")
    InputUtils.setValueByLabelText(wait, "First Name", "John")
    InputUtils.setValueByLabelText(wait, "Last Name", "Doe")
    DateUtils.setValueByLabelText(wait, "Birth Date", "01/15/1990")
    
    # Tab 2: Contact Information
    TabUtils.clickTabByLabelText(wait, "Contact Information")
    InputUtils.setValueByLabelText(wait, "Email", "john.doe@company.com")
    InputUtils.setValueByLabelText(wait, "Phone", "555-123-4567")
    InputUtils.setValueByLabelText(wait, "Address", "123 Main St")
    
    # Tab 3: Employment Details
    TabUtils.clickTabByLabelText(wait, "Employment Details")
    DropdownUtils.selectDropdownValueByLabelText(wait, "Department", "Engineering")
    DropdownUtils.selectDropdownValueByLabelText(wait, "Position", "Software Developer")
    DateUtils.setValueByLabelText(wait, "Start Date", ComponentUtils.today())
    
    # Tab 4: Review and Submit
    TabUtils.clickTabByLabelText(wait, "Review and Submit")
    ButtonUtils.clickByLabelText(wait, "Submit Application")
```

## ComponentDriver

The `ComponentDriver` provides a unified interface for interacting with all component types.

### Usage

```python
from robo_appian.controllers.ComponentDriver import ComponentDriver

# Universal component interaction
ComponentDriver.execute(wait, "Input Text", "Set Value", "First Name", "John")
ComponentDriver.execute(wait, "Dropdown", "Select", "Department", "Engineering")
ComponentDriver.execute(wait, "Date", "Set Value", "Start Date", "01/15/2024")
ComponentDriver.execute(wait, "Button", "Click", "Submit", None)
```

### Data-Driven Testing

```python
def test_form_with_data_driver():
    """Use ComponentDriver for data-driven testing"""
    
    # Define test data
    form_data = [
        ("Input Text", "Set Value", "Employee ID", "EMP001"),
        ("Input Text", "Set Value", "First Name", "John"),
        ("Input Text", "Set Value", "Last Name", "Doe"),
        ("Input Text", "Set Value", "Email", "john.doe@company.com"),
        ("Date", "Set Value", "Start Date", ComponentUtils.today()),
        ("Dropdown", "Select", "Department", "Engineering"),
        ("Dropdown", "Select", "Status", "Active"),
        ("Button", "Click", "Save Employee", None)
    ]
    
    # Execute each action
    for component_type, action, label, value in form_data:
        try:
            ComponentDriver.execute(wait, component_type, action, label, value)
            print(f"✅ {action} on {label}: {value}")
        except Exception as e:
            print(f"❌ Failed {action} on {label}: {e}")
            break
```

## Component Integration Patterns

### Chain Operations

```python
def chain_component_operations():
    """Chain multiple component operations together"""
    try:
        # Step 1: Fill basic information
        InputUtils.setValueByLabelText(wait, "Name", "John Doe")
        InputUtils.setValueByLabelText(wait, "Email", "john@company.com")
        
        # Step 2: Select options
        DropdownUtils.selectDropdownValueByLabelText(wait, "Department", "Engineering")
        DropdownUtils.selectDropdownValueByLabelText(wait, "Role", "Developer")
        
        # Step 3: Set dates
        DateUtils.setValueByLabelText(wait, "Start Date", ComponentUtils.today())
        
        # Step 4: Navigate and submit
        TabUtils.clickTabByLabelText(wait, "Review")
        ButtonUtils.clickByLabelText(wait, "Submit")
        
        return True
        
    except Exception as e:
        print(f"Chain operation failed: {e}")
        return False
```

### Conditional Logic

```python
def conditional_form_filling():
    """Fill form based on conditions"""
    
    # Check if optional section is present
    if ComponentUtils.checkComponentExistsByXpath(wait, "//div[@id='optional-section']"):
        TabUtils.clickTabByLabelText(wait, "Additional Information")
        InputUtils.setValueByLabelText(wait, "Additional Notes", "Optional information provided")
    
    # Check employment type and fill accordingly
    employment_type = "Full-time"  # This could come from test data
    DropdownUtils.selectDropdownValueByLabelText(wait, "Employment Type", employment_type)
    
    if employment_type == "Full-time":
        DateUtils.setValueByLabelText(wait, "Start Date", ComponentUtils.today())
        DropdownUtils.selectDropdownValueByLabelText(wait, "Benefits Package", "Standard")
    elif employment_type == "Contract":
        DateUtils.setValueByLabelText(wait, "Contract Start", ComponentUtils.today())
        DateUtils.setValueByLabelText(wait, "Contract End", "12/31/2024")
```

This comprehensive guide covers all core components and their usage patterns. Use these examples as building blocks for your Appian test automation!
