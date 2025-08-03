# Login Test Examples

This section provides comprehensive examples for testing login functionality in Appian applications using Robo Appian.

## Basic Login Test

Here's a simple login test that demonstrates the core concepts:

```python
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from robo_appian.components.InputUtils import InputUtils
from robo_appian.components.ButtonUtils import ButtonUtils
from robo_appian.utils.ComponentUtils import ComponentUtils

def test_basic_login():
    """Test basic login functionality"""
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    
    try:
        # Navigate to login page
        driver.get("https://your-appian-site.com/login")
        
        # Enter credentials
        InputUtils.setValueByLabelText(wait, "Username", "testuser")
        InputUtils.setValueByLabelText(wait, "Password", "password123")
        
        # Click login button
        ButtonUtils.clickByLabelText(wait, "Sign In")
        
        # Verify successful login
        if ComponentUtils.checkComponentExistsByXpath(wait, "//div[contains(@class, 'dashboard')]"):
            print("✅ Login successful!")
            return True
        else:
            print("❌ Login failed!")
            return False
            
    except Exception as e:
        print(f"❌ Login test failed: {e}")
        return False
    finally:
        driver.quit()

if __name__ == "__main__":
    test_basic_login()
```

## Advanced Login Tests

### Multi-User Login Test

```python
def test_multiple_users():
    """Test login with multiple user accounts"""
    users = [
        {"username": "admin", "password": "admin123", "expected_role": "Administrator"},
        {"username": "user1", "password": "user123", "expected_role": "User"},
        {"username": "manager", "password": "mgr123", "expected_role": "Manager"}
    ]
    
    for user in users:
        driver = webdriver.Chrome()
        wait = WebDriverWait(driver, 10)
        
        try:
            driver.get("https://your-appian-site.com/login")
            
            # Login with user credentials
            InputUtils.setValueByLabelText(wait, "Username", user["username"])
            InputUtils.setValueByLabelText(wait, "Password", user["password"])
            ButtonUtils.clickByLabelText(wait, "Sign In")
            
            # Verify role-specific elements
            role_xpath = f"//span[contains(text(), '{user['expected_role']}')]"
            if ComponentUtils.checkComponentExistsByXpath(wait, role_xpath):
                print(f"✅ {user['username']} logged in successfully with {user['expected_role']} role")
            else:
                print(f"❌ {user['username']} login failed or incorrect role")
                
        finally:
            driver.quit()
```

### Login with Error Handling

```python
def test_login_with_error_handling():
    """Test login with comprehensive error handling"""
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    
    try:
        driver.get("https://your-appian-site.com/login")
        
        # Test invalid credentials first
        InputUtils.setValueByLabelText(wait, "Username", "invalid_user")
        InputUtils.setValueByLabelText(wait, "Password", "wrong_password")
        ButtonUtils.clickByLabelText(wait, "Sign In")
        
        # Check for error message
        error_xpath = "//div[contains(@class, 'error') or contains(text(), 'Invalid')]"
        if ComponentUtils.checkComponentExistsByXpath(wait, error_xpath):
            print("✅ Error message displayed for invalid credentials")
            
            # Clear fields and try valid credentials
            InputUtils.setValueByLabelText(wait, "Username", "testuser")
            InputUtils.setValueByLabelText(wait, "Password", "password123")
            ButtonUtils.clickByLabelText(wait, "Sign In")
            
            # Verify successful login
            if ComponentUtils.checkComponentExistsByXpath(wait, "//div[contains(@class, 'dashboard')]"):
                print("✅ Login successful with valid credentials")
            else:
                print("❌ Login failed even with valid credentials")
        else:
            print("❌ No error message displayed for invalid credentials")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
    finally:
        driver.quit()
```

## Integration with Testing Frameworks

### pytest Example

```python
import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

@pytest.fixture(scope="session")
def driver():
    """WebDriver fixture for the test session"""
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

@pytest.fixture
def wait(driver):
    """WebDriverWait fixture"""
    return WebDriverWait(driver, 10)

@pytest.fixture
def login_page(driver):
    """Navigate to login page"""
    driver.get("https://your-appian-site.com/login")
    return driver

class TestLogin:
    """Login test class"""
    
    def test_valid_login(self, driver, wait, login_page):
        """Test login with valid credentials"""
        InputUtils.setValueByLabelText(wait, "Username", "testuser")
        InputUtils.setValueByLabelText(wait, "Password", "password123")
        ButtonUtils.clickByLabelText(wait, "Sign In")
        
        assert ComponentUtils.checkComponentExistsByXpath(wait, "//div[contains(@class, 'dashboard')]")
    
    def test_invalid_login(self, driver, wait, login_page):
        """Test login with invalid credentials"""
        InputUtils.setValueByLabelText(wait, "Username", "invalid")
        InputUtils.setValueByLabelText(wait, "Password", "invalid")
        ButtonUtils.clickByLabelText(wait, "Sign In")
        
        assert ComponentUtils.checkComponentExistsByXpath(wait, "//div[contains(@class, 'error')]")
    
    @pytest.mark.parametrize("username,password,should_succeed", [
        ("admin", "admin123", True),
        ("user1", "user123", True),
        ("invalid", "invalid", False),
        ("", "", False)
    ])
    def test_login_scenarios(self, driver, wait, login_page, username, password, should_succeed):
        """Test multiple login scenarios"""
        InputUtils.setValueByLabelText(wait, "Username", username)
        InputUtils.setValueByLabelText(wait, "Password", password)
        ButtonUtils.clickByLabelText(wait, "Sign In")
        
        if should_succeed:
            assert ComponentUtils.checkComponentExistsByXpath(wait, "//div[contains(@class, 'dashboard')]")
        else:
            assert ComponentUtils.checkComponentExistsByXpath(wait, "//div[contains(@class, 'error')]")
```

### unittest Example

```python
import unittest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

class TestAppianLogin(unittest.TestCase):
    """Login test cases using unittest"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)
        self.driver.get("https://your-appian-site.com/login")
    
    def tearDown(self):
        """Clean up after tests"""
        self.driver.quit()
    
    def test_successful_login(self):
        """Test successful login"""
        InputUtils.setValueByLabelText(self.wait, "Username", "testuser")
        InputUtils.setValueByLabelText(self.wait, "Password", "password123")
        ButtonUtils.clickByLabelText(self.wait, "Sign In")
        
        self.assertTrue(
            ComponentUtils.checkComponentExistsByXpath(
                self.wait, "//div[contains(@class, 'dashboard')]"
            )
        )
    
    def test_failed_login(self):
        """Test failed login"""
        InputUtils.setValueByLabelText(self.wait, "Username", "invalid")
        InputUtils.setValueByLabelText(self.wait, "Password", "invalid")
        ButtonUtils.clickByLabelText(self.wait, "Sign In")
        
        self.assertTrue(
            ComponentUtils.checkComponentExistsByXpath(
                self.wait, "//div[contains(@class, 'error')]"
            )
        )

if __name__ == "__main__":
    unittest.main()
```

## Best Practices for Login Tests

### 1. Use Environment Variables for Credentials

```python
import os

def test_login_with_env_credentials():
    """Use environment variables for test credentials"""
    username = os.getenv("TEST_USERNAME", "default_user")
    password = os.getenv("TEST_PASSWORD", "default_pass")
    
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    
    try:
        driver.get("https://your-appian-site.com/login")
        InputUtils.setValueByLabelText(wait, "Username", username)
        InputUtils.setValueByLabelText(wait, "Password", password)
        ButtonUtils.clickByLabelText(wait, "Sign In")
        
        # Verify login
        assert ComponentUtils.checkComponentExistsByXpath(wait, "//div[contains(@class, 'dashboard')]")
        
    finally:
        driver.quit()
```

### 2. Implement Page Object Pattern

```python
class LoginPage:
    """Page Object for login page"""
    
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait
    
    def navigate_to_login(self):
        """Navigate to login page"""
        self.driver.get("https://your-appian-site.com/login")
    
    def enter_credentials(self, username, password):
        """Enter login credentials"""
        InputUtils.setValueByLabelText(self.wait, "Username", username)
        InputUtils.setValueByLabelText(self.wait, "Password", password)
    
    def click_login(self):
        """Click login button"""
        ButtonUtils.clickByLabelText(self.wait, "Sign In")
    
    def is_login_successful(self):
        """Check if login was successful"""
        return ComponentUtils.checkComponentExistsByXpath(
            self.wait, "//div[contains(@class, 'dashboard')]"
        )
    
    def is_error_displayed(self):
        """Check if error message is displayed"""
        return ComponentUtils.checkComponentExistsByXpath(
            self.wait, "//div[contains(@class, 'error')]"
        )

# Usage
def test_with_page_object():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    login_page = LoginPage(driver, wait)
    
    try:
        login_page.navigate_to_login()
        login_page.enter_credentials("testuser", "password123")
        login_page.click_login()
        
        assert login_page.is_login_successful()
        
    finally:
        driver.quit()
```

### 3. Add Logging and Screenshots

```python
import logging
import time
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_login_with_logging():
    """Login test with comprehensive logging"""
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    
    try:
        logger.info("Starting login test")
        
        # Navigate to login page
        logger.info("Navigating to login page")
        driver.get("https://your-appian-site.com/login")
        
        # Take screenshot of login page
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        driver.save_screenshot(f"login_page_{timestamp}.png")
        logger.info(f"Screenshot saved: login_page_{timestamp}.png")
        
        # Enter credentials
        logger.info("Entering credentials")
        InputUtils.setValueByLabelText(wait, "Username", "testuser")
        InputUtils.setValueByLabelText(wait, "Password", "password123")
        
        # Click login
        logger.info("Clicking login button")
        ButtonUtils.clickByLabelText(wait, "Sign In")
        
        # Verify and screenshot result
        if ComponentUtils.checkComponentExistsByXpath(wait, "//div[contains(@class, 'dashboard')]"):
            logger.info("✅ Login successful")
            driver.save_screenshot(f"login_success_{timestamp}.png")
        else:
            logger.error("❌ Login failed")
            driver.save_screenshot(f"login_failure_{timestamp}.png")
            
    except Exception as e:
        logger.error(f"❌ Login test failed with exception: {e}")
        driver.save_screenshot(f"login_error_{timestamp}.png")
    finally:
        driver.quit()
        logger.info("Login test completed")
```

## Troubleshooting Login Issues

### Common Problems and Solutions

#### 1. Login Button Not Found

```python
# Problem: Button label might be different
# Try different variations
login_button_labels = ["Sign In", "Login", "Log In", "Submit", "Enter"]

for label in login_button_labels:
    if ComponentUtils.checkComponentExistsByXpath(wait, f"//button[contains(text(), '{label}')]"):
        ButtonUtils.clickByLabelText(wait, label)
        break
```

#### 2. Input Fields Not Found

```python
# Problem: Input labels might be different
# Check for various label formats
username_labels = ["Username", "User Name", "Email", "Login ID", "User ID"]
password_labels = ["Password", "Pass", "Secret"]

for label in username_labels:
    try:
        InputUtils.setValueByLabelText(wait, label, "testuser")
        break
    except:
        continue
```

#### 3. Page Load Issues

```python
# Problem: Page takes time to load
# Add explicit waits
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Wait for login form to be present
wait.until(EC.presence_of_element_located((By.XPATH, "//form")))

# Or wait for specific element
wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='text']")))
```

This comprehensive guide should help you implement robust login tests for your Appian applications!
