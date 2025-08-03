# DateUtils

The `DateUtils` class provides specialized methods for interacting with date picker components in Appian applications. It handles the unique challenges of date input fields, including date picker interactions and various date format requirements.

## Overview

DateUtils is designed to handle Appian's date components, providing reliable methods to:

- Set date values using visible label text
- Click date components to open date pickers
- Handle various date formats and input methods
- Manage Appian's specialized date input structures

## Class Methods

### setValueByLabelText()

Sets a date value in a date component by its visible label text.


**Parameters:**
- `wait` (WebDriverWait): Selenium WebDriverWait instance for element waiting
- `label` (str): The visible text label of the date component
- `value` (str): The date value to set (format depends on field configuration)

**Returns:**
- `WebElement`: The date input component after setting the value

**Usage Example:**
```python
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from robo_appian.components.DateUtils import DateUtils

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

# Set start date
DateUtils.setValueByLabelText(wait, "Start Date", "01/15/2024")

# Set end date
DateUtils.setValueByLabelText(wait, "End Date", "12/31/2024")

# Set birth date
DateUtils.setValueByLabelText(wait, "Date of Birth", "05/20/1990")

# Set appointment date and time
DateUtils.setValueByLabelText(wait, "Appointment Date", "03/15/2024")
```

---

### clickByLabelText()

Clicks on a date component to open the date picker interface.

**Signature:**
```python
@staticmethod
def clickByLabelText(wait: WebDriverWait, label: str) -> WebElement
```

**Parameters:**
- `wait` (WebDriverWait): Selenium WebDriverWait instance for element waiting
- `label` (str): The visible text label of the date component

**Returns:**
- `WebElement`: The date input component that was clicked

**Usage Example:**
```python
# Click to open date picker
DateUtils.clickByLabelText(wait, "Start Date")

# After clicking, you can interact with the date picker
# (Note: Additional methods would be needed for date picker navigation)

# Alternative: Set value directly without opening picker
DateUtils.setValueByLabelText(wait, "Start Date", "01/15/2024")
```

## Date Format Support

DateUtils supports various date formats depending on your Appian application configuration:

### Common Date Formats

```python
# MM/DD/YYYY format (US)
DateUtils.setValueByLabelText(wait, "Start Date", "01/15/2024")

# DD/MM/YYYY format (European)
DateUtils.setValueByLabelText(wait, "Start Date", "15/01/2024")

# YYYY-MM-DD format (ISO)
DateUtils.setValueByLabelText(wait, "Start Date", "2024-01-15")

# MM-DD-YYYY format
DateUtils.setValueByLabelText(wait, "Start Date", "01-15-2024")

# Date with text month
DateUtils.setValueByLabelText(wait, "Start Date", "January 15, 2024")
```

### Date and Time Formats

```python
# Date with time (12-hour format)
DateUtils.setValueByLabelText(wait, "Appointment", "01/15/2024 2:30 PM")

# Date with time (24-hour format)
DateUtils.setValueByLabelText(wait, "Appointment", "01/15/2024 14:30")

# ISO datetime format
DateUtils.setValueByLabelText(wait, "Timestamp", "2024-01-15T14:30:00")
```

## Best Practices

### Determine Required Format

**Check field format requirements** before setting values:
```python
# Test with different formats to determine what's accepted
formats_to_try = [
    "01/15/2024",      # MM/DD/YYYY
    "15/01/2024",      # DD/MM/YYYY  
    "2024-01-15",      # YYYY-MM-DD
    "Jan 15, 2024"     # Text format
]

for date_format in formats_to_try:
    try:
        DateUtils.setValueByLabelText(wait, "Start Date", date_format)
        print(f"Accepted format: {date_format}")
        break
    except Exception:
        continue
```

### Validate Date Input

**Verify date was set correctly**:
```python
# Set date and verify
date_component = DateUtils.setValueByLabelText(wait, "Start Date", "01/15/2024")

# Check if value was set correctly
current_value = date_component.get_attribute("value")
print(f"Date field value: {current_value}")

# Verify expected format
expected_date = "01/15/2024"
assert expected_date in current_value, f"Expected {expected_date}, got {current_value}"
```

### Handle Date Picker Interactions

For complex date picker interactions:
```python
def select_date_from_picker(wait, label, target_date):
    """
    Example function for complex date picker interaction
    """
    # Open the date picker
    DateUtils.clickByLabelText(wait, label)
    
    # Custom logic for navigating date picker
    # (Implementation would depend on specific date picker structure)
    
    # Alternative: Use direct value setting
    DateUtils.setValueByLabelText(wait, label, target_date)
```

## Common Use Cases

### Event Scheduling
```python
# Schedule meeting
DateUtils.setValueByLabelText(wait, "Meeting Date", "03/15/2024")
DateUtils.setValueByLabelText(wait, "Start Time", "10:00 AM")
DateUtils.setValueByLabelText(wait, "End Time", "11:30 AM")
```

### Date Range Selection
```python
# Set date range for reports
DateUtils.setValueByLabelText(wait, "From Date", "01/01/2024")
DateUtils.setValueByLabelText(wait, "To Date", "01/31/2024")

# Generate report
ButtonUtils.clickByLabelText(wait, "Generate Report")
```

### Employee Information
```python
# Employee details with dates
InputUtils.setValueByLabelText(wait, "Employee Name", "John Doe")
DateUtils.setValueByLabelText(wait, "Hire Date", "01/15/2024")
DateUtils.setValueByLabelText(wait, "Date of Birth", "05/20/1990")
DropdownUtils.selectDropdownValueByLabelText(wait, "Department", "Engineering")
```

### Project Timeline
```python
# Project dates
InputUtils.setValueByLabelText(wait, "Project Name", "Website Redesign")
DateUtils.setValueByLabelText(wait, "Start Date", "02/01/2024")
DateUtils.setValueByLabelText(wait, "Expected End Date", "05/31/2024")
DateUtils.setValueByLabelText(wait, "Milestone Date", "03/15/2024")
```

### Financial Records
```python
# Invoice dates
InputUtils.setValueByLabelText(wait, "Invoice Number", "INV-2024-001")
DateUtils.setValueByLabelText(wait, "Invoice Date", "01/15/2024")
DateUtils.setValueByLabelText(wait, "Due Date", "02/14/2024")
InputUtils.setValueByLabelText(wait, "Amount", "1500.00")
```

## Technical Details

### Date Component Location

DateUtils uses a specific XPath strategy to locate date inputs:
```xpath
.//div[./div/label[text()="{label}"]]/div/div/div/input
```

This XPath:
- Finds the label element with exact text match
- Navigates to the associated input element
- Handles Appian's nested div structure for date components

### Integration with InputUtils

DateUtils leverages `InputUtils._setValueByComponent()` for value setting:
1. **Clear existing value** using `clear()`
2. **Set new value** using `send_keys()`
3. **Return component** for further operations

### Error Handling

Comprehensive error handling for date component interactions:
- Element not found exceptions
- Timeout exceptions for dynamic loading
- Value setting validation

## Troubleshooting

### Common Issues

**Date Component Not Found:**
```
Exception: Could not find clickable date component with label 'Start Date'
```
**Solutions:**
- Verify exact label text (check for colons, asterisks, spacing)
- Ensure date component is visible and not disabled
- Check if component is inside collapsed sections or tabs
- Wait for any dynamic content to load

**Invalid Date Format:**
```
Date not accepted or field shows error
```
**Solutions:**
- Check application's expected date format
- Try different format variations
- Verify locale settings in Appian application
- Check field validation rules

**Date Picker Not Opening:**
```
Date picker interface doesn't appear after click
```
**Solutions:**
- Verify element is clickable and not disabled
- Check if date picker is already open
- Ensure no JavaScript errors are preventing interaction
- Try clicking on the calendar icon if present

### Debugging Tips

1. **Inspect Date Field Structure**:
   ```html
   <div>
     <div>
       <label>Start Date</label>
     </div>
     <div>
       <div>
         <div>
           <input type="text" placeholder="MM/DD/YYYY">
         </div>
       </div>
     </div>
   </div>
   ```

2. **Check Date Format Requirements**:
   - Look for placeholder text indicating expected format
   - Check field validation messages
   - Test with known valid dates first

3. **Verify Component State**:
   - Ensure field is enabled and editable
   - Check if field has focus after clicking
   - Verify no JavaScript validation prevents input

## Integration Examples

### With pytest and Date Validation
```python
import pytest
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from robo_appian.components.DateUtils import DateUtils

class TestDateInputs:
    def setup_method(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)
    
    def teardown_method(self):
        self.driver.quit()
    
    def test_future_date_selection(self):
        self.driver.get("https://your-appian-app.com")
        
        # Calculate future date
        future_date = datetime.now() + timedelta(days=30)
        date_string = future_date.strftime("%m/%d/%Y")
        
        # Set future date
        DateUtils.setValueByLabelText(self.wait, "Appointment Date", date_string)
        
        # Verify date was set
        date_component = self.driver.find_element(By.XPATH, 
            './/div[./div/label[text()="Appointment Date"]]/div/div/div/input')
        assert date_string in date_component.get_attribute("value")
```

### With Page Object Model
```python
class EventRegistrationPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def schedule_event(self, event_name, start_date, end_date, start_time):
        InputUtils.setValueByLabelText(self.wait, "Event Name", event_name)
        DateUtils.setValueByLabelText(self.wait, "Start Date", start_date)
        DateUtils.setValueByLabelText(self.wait, "End Date", end_date)
        DateUtils.setValueByLabelText(self.wait, "Start Time", start_time)
    
    def set_registration_deadline(self, deadline_date):
        DateUtils.setValueByLabelText(self.wait, "Registration Deadline", deadline_date)
```

### With Date Utility Functions
```python
from datetime import datetime, timedelta

class DateHelper:
    @staticmethod
    def format_date_for_appian(date_obj, format_type="US"):
        """Convert datetime object to Appian-compatible string"""
        if format_type == "US":
            return date_obj.strftime("%m/%d/%Y")
        elif format_type == "EU":
            return date_obj.strftime("%d/%m/%Y")
        elif format_type == "ISO":
            return date_obj.strftime("%Y-%m-%d")
    
    @staticmethod
    def get_business_days_from_now(days):
        """Calculate business days from current date"""
        current = datetime.now()
        business_days = 0
        while business_days < days:
            current += timedelta(days=1)
            if current.weekday() < 5:  # Monday = 0, Friday = 4
                business_days += 1
        return current

# Usage with DateUtils
future_business_date = DateHelper.get_business_days_from_now(10)
formatted_date = DateHelper.format_date_for_appian(future_business_date, "US")
DateUtils.setValueByLabelText(wait, "Due Date", formatted_date)
```

## Related Components

- **[InputUtils](input-utils.md)** - For general input field interactions
- **[ButtonUtils](button-utils.md)** - For form submission after date entry
- **[DropdownUtils](dropdown-utils.md)** - For date-related dropdown selections
- **[ComponentDriver](component-driver.md)** - For universal component interactions

---

*DateUtils provides specialized date handling capabilities for Appian applications, managing the complexity of date format requirements and date picker interactions while maintaining reliability and ease of use.*
