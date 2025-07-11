# Examples

This page provides comprehensive examples of using Robo Appian for various Appian automation scenarios.

## Basic Setup

```python
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from robo_appian import *

# Setup Chrome driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
wait = WebDriverWait(driver, 10)

try:
    # Navigate to your Appian application
    driver.get("https://your-appian-app.com")
    
    # Your automation code here
    
finally:
    driver.quit()
```

## Form Interaction Examples

### Login Form

```python
from robo_appian import InputUtils, ButtonUtils

# Fill in login credentials
InputUtils.set_setInputValuetext(wait, "Username", "john.doe")
InputUtils.setInputValue(wait, "Password", "secure_password")

# Click login button
ButtonUtils.click(wait, "Sign In")
```

### Complex Form with Various Components

```python
from robo_appian import InputUtils, DropdownUtils, DateUtils, ButtonUtils

# Fill text inputs
InputUtils.setInputValue(wait, "First Name", "John")
InputUtils.setInputValue(wait, "Last Name", "Doe")
InputUtils.setInputValue(wait, "Email", "john.doe@company.com")

# Select from dropdown
DropdownUtils.select_by_text(wait, "Department", "Engineering")

# Set date
DateUtils.set_date(wait, "Start Date", "01/15/2024")

# Submit form
ButtonUtils.click(wait, "Submit")
```

## Table Operations

### Reading Table Data

```python
from robo_appian import TableUtils

# Get all rows in a table
table_data = TableUtils.get_all_table_data(wait)
print(f"Found {len(table_data)} rows")

# Get specific cell value
cell_value = TableUtils.get_cell_text(wait, 1, "Employee Name")
print(f"Employee: {cell_value}")
```

### Table Actions

```python
from robo_appian import TableUtils

# Click a link in a table cell
TableUtils.click_cell_link(wait, "Actions", 1, "Edit")

# Click a specific row
TableUtils.click_row(wait, 2, "Employee Name")
```

## Navigation Examples

### Tab Navigation

```python
from robo_appian import TabUtils

# Switch to different tabs
TabUtils.click(wait, "Personal Info")
TabUtils.click(wait, "Employment Details")
TabUtils.click(wait, "Documents")
```

### Link Navigation

```python
from robo_appian import LinkUtils

# Click navigation links
LinkUtils.click(wait, "Dashboard")
LinkUtils.click(wait, "Reports")
LinkUtils.click(wait, "Settings")
```

## Data Entry Workflows

### Employee Registration

```python
def register_employee(wait, employee_data):
    """Complete employee registration workflow"""
    
    # Personal Information
    InputUtils.set_text(wait, "First Name", employee_data["first_name"])
    InputUtils.set_text(wait, "Last Name", employee_data["last_name"])
    DateUtils.set_date(wait, "Birth Date", employee_data["birth_date"])
    
    # Employment Details
    TabUtils.click(wait, "Employment")
    DropdownUtils.select_by_text(wait, "Department", employee_data["department"])
    DropdownUtils.select_by_text(wait, "Position", employee_data["position"])
    DateUtils.set_date(wait, "Start Date", employee_data["start_date"])
    
    # Submit
    ButtonUtils.click(wait, "Save Employee")

# Usage
employee_data = {
    "first_name": "Jane",
    "last_name": "Smith", 
    "birth_date": "03/15/1990",
    "department": "Marketing",
    "position": "Manager",
    "start_date": "02/01/2024"
}

register_employee(wait, employee_data)
```

## Error Handling

### Robust Automation with Error Handling

```python
from selenium.common.exceptions import TimeoutException
from robo_appian import ButtonUtils, InputUtils
from robo_appian.utils.exceptions.MyCustomError import MyCustomError

def safe_form_submission(wait, form_data):
    """Submit form with proper error handling"""
    try:
        # Fill form fields
        for field_name, value in form_data.items():
            InputUtils.set_text(wait, field_name, value)
        
        # Submit form
        ButtonUtils.click(wait, "Submit")
        
        # Verify success (look for success message or redirect)
        success_element = wait.until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'success')]"))
        )
        return True
        
    except TimeoutException as e:
        print(f"Timeout occurred: {e}")
        return False
    except MyCustomError as e:
        print(f"Custom error occurred: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

# Usage
form_data = {
    "Name": "Test User",
    "Email": "test@example.com"
}

if safe_form_submission(wait, form_data):
    print("Form submitted successfully!")
else:
    print("Form submission failed!")
```

## Best Practices

### 1. Use Page Object Model

```python
class LoginPage:
    def __init__(self, wait):
        self.wait = wait
    
    def login(self, username, password):
        InputUtils.set_text(self.wait, "Username", username)
        InputUtils.set_text(self.wait, "Password", password)
        ButtonUtils.click(self.wait, "Sign In")
    
    def is_logged_in(self):
        try:
            # Check for logout button or user profile
            LogoutButton = ButtonUtils.find(self.wait, "Logout")
            return True
        except:
            return False

# Usage
login_page = LoginPage(wait)
login_page.login("user@company.com", "password123")
assert login_page.is_logged_in(), "Login failed"
```

### 2. Create Reusable Test Data

```python
# test_data.py
TEST_USERS = {
    "admin": {
        "username": "admin@company.com",
        "password": "admin123",
        "role": "Administrator"
    },
    "user": {
        "username": "user@company.com", 
        "password": "user123",
        "role": "Standard User"
    }
}

SAMPLE_EMPLOYEES = [
    {
        "first_name": "John",
        "last_name": "Doe",
        "department": "Engineering",
        "position": "Developer"
    },
    {
        "first_name": "Jane",
        "last_name": "Smith",
        "department": "Marketing", 
        "position": "Manager"
    }
]
```

### 3. Use Configuration Files

```python
# config.py
import os

class Config:
    BASE_URL = os.getenv("APPIAN_URL", "https://your-appian-app.com")
    TIMEOUT = int(os.getenv("TIMEOUT", "10"))
    BROWSER = os.getenv("BROWSER", "chrome")
    HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"

# Usage in tests
from config import Config

driver.get(Config.BASE_URL)
wait = WebDriverWait(driver, Config.TIMEOUT)
```

## Troubleshooting

### Common Issues and Solutions

1. **Element not found**: Increase wait timeout or check element locators
2. **Stale element reference**: Re-find elements after page changes
3. **Click intercepted**: Scroll element into view before clicking
4. **Timeout exceptions**: Verify element visibility and page load times

### Debug Mode

```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Add explicit waits for debugging
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Wait for specific conditions
wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Submit']")))
```
