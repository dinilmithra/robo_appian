# Quick Start

Get up and running with Robo Appian in just a few minutes! This guide will walk you through creating your first automated test for an Appian application.

## Prerequisites

Make sure you have:

- [x] Python 3.12+ installed
- [x] Robo Appian installed (`pip install robo_appian`)
- [x] Chrome browser and ChromeDriver set up
- [x] Access to an Appian application for testing

!!! tip "Need help with installation?"
    Check out our [Installation Guide](installation.md) if you haven't set up Robo Appian yet.

## Your First Test

Let's create a simple login test to demonstrate Robo Appian's capabilities.

### Step 1: Basic Setup

Create a new Python file called `first_test.py`:

```python title="first_test.py"
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from robo_appian.components.InputUtils import InputUtils
from robo_appian.components.ButtonUtils import ButtonUtils
from robo_appian.utils.ComponentUtils import ComponentUtils

def test_appian_login():
    """Simple login test using Robo Appian"""
    
    # Initialize WebDriver with 10-second timeout
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    
    try:
        # Navigate to your Appian login page
        driver.get("https://your-appian-site.com/login")
        
        # Enter credentials using label-based methods
        InputUtils.setValueByLabelText(wait, "Username", "your_username")
        InputUtils.setValueByLabelText(wait, "Password", "your_password")
        
        # Click the login button
        ButtonUtils.clickByLabelText(wait, "Sign In")
        
        # Verify login was successful
        if ComponentUtils.checkComponentExistsByXpath(wait, "//div[contains(@class, 'dashboard')]"):
            print("✅ Login successful!")
        else:
            print("❌ Login failed!")
            
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
    finally:
        # Always close the browser
        driver.quit()

if __name__ == "__main__":
    test_appian_login()
```

### Step 2: Run Your Test

```bash
python first_test.py
```

### Step 3: Understanding the Code

Let's break down what each part does:

=== "WebDriver Setup"
    ```python
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    ```
    
    - Creates a Chrome browser instance
    - Sets up a 10-second wait timeout for element interactions

=== "Label-Based Interaction"
    ```python
    InputUtils.setValueByLabelText(wait, "Username", "your_username")
    ```
    
    - Finds the input field with label "Username"
    - Sets the value to "your_username"
    - Much simpler than complex XPath selectors!

=== "Component Validation"
    ```python
    ComponentUtils.checkComponentExistsByXpath(wait, "//div[contains(@class, 'dashboard')]")
    ```
    
    - Checks if a dashboard element exists
    - Returns `True` if found, `False` otherwise

## Common Patterns

Here are some common patterns you'll use frequently:

### Form Filling

```python
def fill_employee_form():
    # Personal information
    InputUtils.setValueByLabelText(wait, "First Name", "John")
    InputUtils.setValueByLabelText(wait, "Last Name", "Doe")
    InputUtils.setValueByLabelText(wait, "Email", "john.doe@company.com")
    
    # Work information
    DateUtils.setValueByLabelText(wait, "Start Date", "01/15/2024")
    DropdownUtils.selectDropdownValueByLabelText(wait, "Department", "Engineering")
    
    # Submit the form
    ButtonUtils.clickByLabelText(wait, "Save Employee")
```

### Data Validation

```python
def validate_employee_data():
    # Check if employee was saved successfully
    success_xpath = "//div[contains(text(), 'Employee saved successfully')]"
    if ComponentUtils.checkComponentExistsByXpath(wait, success_xpath):
        print("✅ Employee saved!")
        return True
    else:
        print("❌ Employee save failed!")
        return False
```

### Table Interaction

```python
def get_employee_count():
    # Find the employee table
    table = TableUtils.findTableByColumnName(wait, "Employee ID")
    count = TableUtils.rowCount(table)
    print(f"Total employees: {count}")
    return count
```

## Best Practices

### 1. Use Try-Catch Blocks

Always wrap your test code in try-catch blocks:

```python
try:
    # Your test code here
    InputUtils.setValueByLabelText(wait, "Username", "testuser")
    ButtonUtils.clickByLabelText(wait, "Submit")
except Exception as e:
    print(f"Test failed: {e}")
finally:
    driver.quit()  # Always close the browser
```

### 2. Use Descriptive Variable Names

```python
# Good
login_button = "Sign In"
username_field = "Username"

# Not so good  
btn = "Sign In"
field1 = "Username"
```

### 3. Set Appropriate Timeouts

```python
# For slow applications
wait = WebDriverWait(driver, 20)

# For quick checks
wait_short = WebDriverWait(driver, 5)
```

### 4. Check Component Existence for Optional Elements

```python
# Check if optional field exists before interacting
if ComponentUtils.checkComponentExistsByXpath(wait, "//input[@id='optional-field']"):
    InputUtils.setValueByLabelText(wait, "Optional Field", "value")
```

## Advanced Example

Here's a more comprehensive example that demonstrates multiple Robo Appian features:

```python title="advanced_example.py"
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from robo_appian.components import *
from robo_appian.utils.ComponentUtils import ComponentUtils
from robo_appian.controllers.ComponentDriver import ComponentDriver

def test_employee_management_workflow():
    """Complete employee management test workflow"""
    
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    
    try:
        # Step 1: Login
        driver.get("https://your-appian-app.com")
        InputUtils.setValueByLabelText(wait, "Username", "admin")
        InputUtils.setValueByLabelText(wait, "Password", "password")
        ButtonUtils.clickByLabelText(wait, "Sign In")
        
        # Step 2: Navigate to employee section
        TabUtils.clickTabByLabelText(wait, "Employees")
        
        # Step 3: Add new employee using ComponentDriver
        ButtonUtils.clickByLabelText(wait, "Add Employee")
        
        employee_data = [
            ("Input Text", "Set Value", "Employee ID", "EMP001"),
            ("Input Text", "Set Value", "First Name", "John"),
            ("Input Text", "Set Value", "Last Name", "Doe"),
            ("Input Text", "Set Value", "Email", "john.doe@company.com"),
            ("Date", "Set Value", "Start Date", ComponentUtils.today()),
            ("Dropdown", "Select", "Department", "Engineering"),
            ("Dropdown", "Select", "Status", "Active"),
            ("Button", "Click", "Save Employee", None)
        ]
        
        for component_type, action, label, value in employee_data:
            ComponentDriver.execute(wait, component_type, action, label, value)
        
        # Step 4: Verify employee was added
        if ComponentUtils.checkComponentExistsByXpath(wait, "//div[contains(text(), 'Employee saved')]"):
            print("✅ Employee added successfully!")
            
            # Step 5: Verify in employee table
            table = TableUtils.findTableByColumnName(wait, "Employee ID")
            row_count = TableUtils.rowCount(table)
            print(f"✅ Total employees: {row_count}")
            
            # Find our new employee
            for row in range(1, row_count + 1):
                emp_id = TableUtils.findComponentFromTableCell(wait, row, "Employee ID").text
                if emp_id == "EMP001":
                    name = TableUtils.findComponentFromTableCell(wait, row, "Name").text
                    print(f"✅ Found employee: {name}")
                    break
        else:
            print("❌ Employee addition failed!")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    test_employee_management_workflow()
```

## What's Next?

Now that you've created your first test, here are some next steps:

<div class="grid cards" markdown>

-   :material-book-open-page-variant:{ .lg .middle } __Learn Core Components__

    ---

    Dive deeper into each component type and their capabilities

    [:octicons-arrow-right-24: Core Components](../user-guide/components.md)

-   :material-code-braces:{ .lg .middle } __Explore Examples__

    ---

    See real-world examples and common patterns

    [:octicons-arrow-right-24: Examples](../examples/login.md)

-   :material-api:{ .lg .middle } __API Reference__

    ---

    Complete reference for all classes and methods

    [:octicons-arrow-right-24: API Reference](../api/component-utils.md)

-   :material-test-tube:{ .lg .middle } __Testing Frameworks__

    ---

    Learn how to integrate with pytest and unittest

    [:octicons-arrow-right-24: Testing Frameworks](../frameworks/pytest.md)

</div>

## Common Issues

### Issue: Element Not Found

**Problem**: `Element with label 'Username' not found`

**Solutions**:
1. Check if the label text is exactly correct (case-sensitive)
2. Increase the wait timeout
3. Ensure the page has fully loaded

```python
# Increase timeout
wait = WebDriverWait(driver, 20)

# Wait for page to load
time.sleep(2)  # Sometimes needed for complex Appian pages
```

### Issue: Element Not Clickable

**Problem**: `Element is not clickable at point (x, y)`

**Solutions**:
1. Scroll the element into view
2. Wait for overlaying elements to disappear
3. Use JavaScript click as fallback

```python
# Scroll to element
driver.execute_script("arguments[0].scrollIntoView();", element)
```

### Issue: Stale Element Reference

**Problem**: `StaleElementReferenceException`

**Solution**: Always use Robo Appian methods instead of storing element references:

```python
# Good - finds element fresh each time
ButtonUtils.clickByLabelText(wait, "Submit")

# Avoid - storing element references
element = driver.find_element(By.ID, "submit-btn")
element.click()  # May become stale
```

Ready to build more sophisticated tests? Continue to the [User Guide](../user-guide/overview.md) for detailed component documentation!
