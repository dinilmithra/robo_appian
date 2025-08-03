# Your First Test

This guide will walk you through creating your very first Robo Appian test step by step. By the end, you'll have a working test that demonstrates the core concepts of Appian test automation.

## What We'll Build

We'll create a comprehensive test that:

1. Logs into an Appian application
2. Navigates to a form
3. Fills out employee information
4. Submits the form
5. Validates the results

## Step-by-Step Tutorial

### Step 1: Set Up Your Environment

First, create a new directory for your test project:

```bash
mkdir my_first_appian_test
cd my_first_appian_test
```

Create a Python file for your test:

```bash
touch test_employee_form.py
```

### Step 2: Import Required Modules

Open `test_employee_form.py` and add the necessary imports:

```python title="test_employee_form.py"
# Selenium imports
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

# Robo Appian imports
from robo_appian.components.InputUtils import InputUtils
from robo_appian.components.ButtonUtils import ButtonUtils
from robo_appian.components.DropdownUtils import DropdownUtils
from robo_appian.components.DateUtils import DateUtils
from robo_appian.components.TabUtils import TabUtils
from robo_appian.utils.ComponentUtils import ComponentUtils

# Standard library imports
import time
```

### Step 3: Create the Test Function

Add the main test function:

```python
def test_employee_form():
    """
    Test that creates a new employee record in Appian
    """
    print("🚀 Starting employee form test...")
    
    # Initialize WebDriver
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    
    try:
        # We'll add test steps here
        pass
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False
    finally:
        driver.quit()
        
    return True
```

### Step 4: Add Login Functionality

Replace the `pass` statement with login logic:

```python
try:
    # Step 1: Navigate to the application
    print("📱 Navigating to Appian application...")
    driver.get("https://your-appian-site.com/login")
    
    # Step 2: Log in
    print("🔐 Logging in...")
    InputUtils.setValueByLabelText(wait, "Username", "testuser")
    InputUtils.setValueByLabelText(wait, "Password", "password123")
    ButtonUtils.clickByLabelText(wait, "Sign In")
    
    # Step 3: Verify login success
    print("✅ Checking login status...")
    if ComponentUtils.checkComponentExistsByXpath(wait, "//div[contains(@class, 'dashboard')]"):
        print("✅ Login successful!")
    else:
        raise Exception("Login failed - dashboard not found")
```

### Step 5: Navigate to Employee Form

Add navigation logic after the login verification:

```python
    # Step 4: Navigate to employee section
    print("📋 Navigating to employee form...")
    TabUtils.clickTabByLabelText(wait, "Human Resources")
    ButtonUtils.clickByLabelText(wait, "Add New Employee")
    
    # Wait for form to load
    time.sleep(2)
    print("✅ Employee form loaded")
```

### Step 6: Fill Out the Form

Add form filling logic:

```python
    # Step 5: Fill out employee information
    print("📝 Filling out employee form...")
    
    # Personal Information
    InputUtils.setValueByLabelText(wait, "Employee ID", "EMP2024001")
    InputUtils.setValueByLabelText(wait, "First Name", "John")
    InputUtils.setValueByLabelText(wait, "Last Name", "Doe")
    InputUtils.setValueByLabelText(wait, "Email", "john.doe@company.com")
    InputUtils.setValueByLabelText(wait, "Phone Number", "555-123-4567")
    
    # Work Information
    DateUtils.setValueByLabelText(wait, "Start Date", ComponentUtils.today())
    DropdownUtils.selectDropdownValueByLabelText(wait, "Department", "Engineering")
    DropdownUtils.selectDropdownValueByLabelText(wait, "Position", "Software Developer")
    DropdownUtils.selectDropdownValueByLabelText(wait, "Employment Type", "Full-time")
    DropdownUtils.selectDropdownValueByLabelText(wait, "Status", "Active")
    
    # Address Information
    InputUtils.setValueByLabelText(wait, "Street Address", "123 Main Street")
    InputUtils.setValueByLabelText(wait, "City", "San Francisco")
    DropdownUtils.selectDropdownValueByLabelText(wait, "State", "California")
    InputUtils.setValueByLabelText(wait, "ZIP Code", "94102")
    
    print("✅ Form filled successfully")
```

### Step 7: Submit and Validate

Add submission and validation logic:

```python
    # Step 6: Submit the form
    print("💾 Submitting employee form...")
    ButtonUtils.clickByLabelText(wait, "Save Employee")
    
    # Step 7: Validate submission
    print("🔍 Validating form submission...")
    
    # Check for success message
    success_xpath = "//div[contains(text(), 'Employee created successfully')]"
    if ComponentUtils.checkComponentExistsByXpath(wait, success_xpath):
        print("✅ Employee created successfully!")
        
        # Optional: Verify the employee appears in the list
        TabUtils.clickTabByLabelText(wait, "Employee List")
        
        # Check if our employee appears in the table
        employee_xpath = "//td[contains(text(), 'EMP2024001')]"
        if ComponentUtils.checkComponentExistsByXpath(wait, employee_xpath):
            print("✅ Employee found in employee list!")
        else:
            print("⚠️ Employee not found in list, but creation was successful")
    else:
        raise Exception("Employee creation failed - no success message found")
    
    print("🎉 Test completed successfully!")
```

### Step 8: Add Main Execution Block

Add the execution block at the end of the file:

```python
if __name__ == "__main__":
    success = test_employee_form()
    if success:
        print("\n🎊 All tests passed! 🎊")
    else:
        print("\n💥 Test failed! 💥")
```

## Complete Code

Here's the complete test file:

```python title="test_employee_form.py"
# Selenium imports
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

# Robo Appian imports
from robo_appian.components.InputUtils import InputUtils
from robo_appian.components.ButtonUtils import ButtonUtils
from robo_appian.components.DropdownUtils import DropdownUtils
from robo_appian.components.DateUtils import DateUtils
from robo_appian.components.TabUtils import TabUtils
from robo_appian.utils.ComponentUtils import ComponentUtils

# Standard library imports
import time

def test_employee_form():
    """
    Test that creates a new employee record in Appian
    """
    print("🚀 Starting employee form test...")
    
    # Initialize WebDriver
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    
    try:
        # Step 1: Navigate to the application
        print("📱 Navigating to Appian application...")
        driver.get("https://your-appian-site.com/login")
        
        # Step 2: Log in
        print("🔐 Logging in...")
        InputUtils.setValueByLabelText(wait, "Username", "testuser")
        InputUtils.setValueByLabelText(wait, "Password", "password123")
        ButtonUtils.clickByLabelText(wait, "Sign In")
        
        # Step 3: Verify login success
        print("✅ Checking login status...")
        if ComponentUtils.checkComponentExistsByXpath(wait, "//div[contains(@class, 'dashboard')]"):
            print("✅ Login successful!")
        else:
            raise Exception("Login failed - dashboard not found")
        
        # Step 4: Navigate to employee section
        print("📋 Navigating to employee form...")
        TabUtils.clickTabByLabelText(wait, "Human Resources")
        ButtonUtils.clickByLabelText(wait, "Add New Employee")
        
        # Wait for form to load
        time.sleep(2)
        print("✅ Employee form loaded")
        
        # Step 5: Fill out employee information
        print("📝 Filling out employee form...")
        
        # Personal Information
        InputUtils.setValueByLabelText(wait, "Employee ID", "EMP2024001")
        InputUtils.setValueByLabelText(wait, "First Name", "John")
        InputUtils.setValueByLabelText(wait, "Last Name", "Doe")
        InputUtils.setValueByLabelText(wait, "Email", "john.doe@company.com")
        InputUtils.setValueByLabelText(wait, "Phone Number", "555-123-4567")
        
        # Work Information
        DateUtils.setValueByLabelText(wait, "Start Date", ComponentUtils.today())
        DropdownUtils.selectDropdownValueByLabelText(wait, "Department", "Engineering")
        DropdownUtils.selectDropdownValueByLabelText(wait, "Position", "Software Developer")
        DropdownUtils.selectDropdownValueByLabelText(wait, "Employment Type", "Full-time")
        DropdownUtils.selectDropdownValueByLabelText(wait, "Status", "Active")
        
        # Address Information
        InputUtils.setValueByLabelText(wait, "Street Address", "123 Main Street")
        InputUtils.setValueByLabelText(wait, "City", "San Francisco")
        DropdownUtils.selectDropdownValueByLabelText(wait, "State", "California")
        InputUtils.setValueByLabelText(wait, "ZIP Code", "94102")
        
        print("✅ Form filled successfully")
        
        # Step 6: Submit the form
        print("💾 Submitting employee form...")
        ButtonUtils.clickByLabelText(wait, "Save Employee")
        
        # Step 7: Validate submission
        print("🔍 Validating form submission...")
        
        # Check for success message
        success_xpath = "//div[contains(text(), 'Employee created successfully')]"
        if ComponentUtils.checkComponentExistsByXpath(wait, success_xpath):
            print("✅ Employee created successfully!")
            
            # Optional: Verify the employee appears in the list
            TabUtils.clickTabByLabelText(wait, "Employee List")
            
            # Check if our employee appears in the table
            employee_xpath = "//td[contains(text(), 'EMP2024001')]"
            if ComponentUtils.checkComponentExistsByXpath(wait, employee_xpath):
                print("✅ Employee found in employee list!")
            else:
                print("⚠️ Employee not found in list, but creation was successful")
        else:
            raise Exception("Employee creation failed - no success message found")
        
        print("🎉 Test completed successfully!")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False
    finally:
        driver.quit()
        
    return True

if __name__ == "__main__":
    success = test_employee_form()
    if success:
        print("\n🎊 All tests passed! 🎊")
    else:
        print("\n💥 Test failed! 💥")
```

## Running Your Test

Execute your test:

```bash
python test_employee_form.py
```

Expected output:
```
🚀 Starting employee form test...
📱 Navigating to Appian application...
🔐 Logging in...
✅ Checking login status...
✅ Login successful!
📋 Navigating to employee form...
✅ Employee form loaded
📝 Filling out employee form...
✅ Form filled successfully
💾 Submitting employee form...
🔍 Validating form submission...
✅ Employee created successfully!
✅ Employee found in employee list!
🎉 Test completed successfully!

🎊 All tests passed! 🎊
```

## Key Concepts Learned

Through this tutorial, you've learned:

### 1. **Label-Based Interaction**
```python
InputUtils.setValueByLabelText(wait, "First Name", "John")
```
Instead of complex XPath selectors, use the visible label text.

### 2. **Component-Specific Methods**
Each UI component type has specialized methods:
- `InputUtils` for text fields
- `DropdownUtils` for dropdowns
- `DateUtils` for date pickers
- `ButtonUtils` for buttons

### 3. **Built-in Validation**
```python
ComponentUtils.checkComponentExistsByXpath(wait, xpath)
```
Easy methods to verify test results.

### 4. **Date Helpers**
```python
ComponentUtils.today()  # Returns today's date in MM/DD/YYYY format
```
Convenient utilities for common scenarios.

### 5. **Error Handling**
Always wrap tests in try-catch blocks and close the browser in the finally block.

## Making It Your Own

To adapt this test for your Appian application:

1. **Update the URL**: Change `https://your-appian-site.com/login` to your actual Appian URL
2. **Adjust Labels**: Use the exact label text from your application
3. **Modify Field Values**: Use appropriate test data for your use case
4. **Update Validation**: Customize success criteria based on your application's behavior

## Common Customizations

### Using Test Data from Files

```python
import json

# Load test data from JSON file
with open('test_data.json', 'r') as f:
    test_data = json.load(f)

InputUtils.setValueByLabelText(wait, "First Name", test_data['employee']['first_name'])
```

### Adding Screenshots on Failure

```python
except Exception as e:
    # Take screenshot on failure
    driver.save_screenshot(f"test_failure_{int(time.time())}.png")
    print(f"❌ Test failed with error: {e}")
    return False
```

### Parameterized Tests

```python
def create_employee(employee_data):
    """Create an employee with given data"""
    for field, value in employee_data.items():
        InputUtils.setValueByLabelText(wait, field, value)

# Test multiple employees
employees = [
    {"First Name": "John", "Last Name": "Doe", "Email": "john@company.com"},
    {"First Name": "Jane", "Last Name": "Smith", "Email": "jane@company.com"}
]

for employee in employees:
    create_employee(employee)
```

## Next Steps

Congratulations! You've created your first Robo Appian test. Here's what to explore next:

<div class="grid cards" markdown>

-   :material-test-tube:{ .lg .middle } __Testing Frameworks__

    ---

    Learn how to organize tests with pytest or unittest

    [:octicons-arrow-right-24: Testing Frameworks](../frameworks/pytest.md)

-   :material-cog:{ .lg .middle } __Advanced Features__

    ---

    Explore ComponentDriver and advanced patterns

    [:octicons-arrow-right-24: Advanced Features](../user-guide/advanced.md)

-   :material-shield-check:{ .lg .middle } __Best Practices__

    ---

    Learn industry best practices for test automation

    [:octicons-arrow-right-24: Best Practices](../user-guide/best-practices.md)

-   :material-bug:{ .lg .middle } __Error Handling__

    ---

    Master error handling and debugging techniques

    [:octicons-arrow-right-24: Error Handling](../user-guide/error-handling.md)

</div>

Happy testing! 🚀
