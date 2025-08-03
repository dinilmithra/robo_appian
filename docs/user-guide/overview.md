# User Guide Overview

Welcome to the Robo Appian User Guide! This comprehensive guide will help you master automated testing of Appian applications using the Robo Appian library.

## What You'll Learn

This user guide covers everything you need to know to become proficient with Robo Appian:

### 🏗️ **Core Concepts**
Understand the fundamental concepts and architecture of Robo Appian, including how it simplifies Appian UI automation.

### 🎯 **Component Mastery**
Learn to use each component utility effectively, from simple buttons to complex data tables.

### 🚀 **Advanced Techniques**
Discover powerful features like the ComponentDriver, data-driven testing, and complex workflow automation.

### 📋 **Best Practices**
Follow industry-proven patterns and practices for maintainable, reliable test automation.

### 🛠️ **Troubleshooting**
Master error handling, debugging techniques, and common issue resolution.

## Guide Structure

<table>
  <tr>
    <td align="center" width="25%">
      <a href="components.md">
        <img src="https://raw.githubusercontent.com/Templarian/MaterialDesign/master/svg/cog.svg" alt="Core Components" width="32" height="32"/><br/>
        <b>Core Components</b>
      </a>
      <div style="font-size: 0.95em; margin-top: 0.5em;">Detailed guide to all Robo Appian components and their usage</div>
      <div><a href="components.md">Go to Core Components &rarr;</a></div>
    </td>
    <td align="center" width="25%">
      <a href="advanced.md">
        <img src="https://raw.githubusercontent.com/Templarian/MaterialDesign/master/svg/rocket.svg" alt="Advanced Features" width="32" height="32"/><br/>
        <b>Advanced Features</b>
      </a>
      <div style="font-size: 0.95em; margin-top: 0.5em;">ComponentDriver, data-driven testing, and complex workflows</div>
      <div><a href="advanced.md">Go to Advanced Features &rarr;</a></div>
    </td>
    <td align="center" width="25%">
      <a href="best-practices.md">
        <img src="https://raw.githubusercontent.com/Templarian/MaterialDesign/master/svg/shield-check.svg" alt="Best Practices" width="32" height="32"/><br/>
        <b>Best Practices</b>
      </a>
      <div style="font-size: 0.95em; margin-top: 0.5em;">Industry best practices for test automation</div>
      <div><a href="best-practices.md">Go to Best Practices &rarr;</a></div>
    </td>
    <td align="center" width="25%">
      <a href="error-handling.md">
        <img src="https://raw.githubusercontent.com/Templarian/MaterialDesign/master/svg/bug.svg" alt="Error Handling" width="32" height="32"/><br/>
        <b>Error Handling</b>
      </a>
      <div style="font-size: 0.95em; margin-top: 0.5em;">Master debugging and error resolution techniques</div>
      <div><a href="error-handling.md">Go to Error Handling &rarr;</a></div>
    </td>
  </tr>
</table>

## Getting the Most from This Guide

### Prerequisites

Before diving into this guide, make sure you have:

- [x] **Robo Appian installed** - See [Installation Guide](../getting-started/installation.md)
- [x] **Basic Python knowledge** - Understanding of functions, classes, and imports
- [x] **Selenium familiarity** - Basic understanding of WebDriver concepts
- [x] **Access to Appian** - An Appian application to test against

### Reading Approach

This guide is designed to be read in order, but you can also jump to specific sections:

=== "Linear Reading"
    **Recommended for beginners**
    
    1. Start with [Core Components](components.md)
    2. Progress through [Advanced Features](advanced.md)  
    3. Study [Best Practices](best-practices.md)
    4. Reference [Error Handling](error-handling.md) as needed

=== "Reference Style"
    **Good for experienced users**
    
    - Use the search function to find specific topics
    - Jump directly to component-specific sections
    - Reference best practices for specific scenarios
    - Consult error handling for troubleshooting

### Learning Tips

!!! tip "Hands-on Practice"
    The best way to learn Robo Appian is by practicing. Try the examples in your own Appian environment.

!!! note "Code Examples"
    All code examples are tested and ready to use. Copy and adapt them for your specific needs.

!!! warning "Version Compatibility"
    This guide is for Robo Appian v0.0.12+. Some features may not be available in older versions.

## Core Philosophy

Understanding Robo Appian's design philosophy will help you use it more effectively:

### 1. **Label-Based Interaction**

Traditional Selenium:
```python
element = driver.find_element(By.XPATH, "//div[@class='appian-component']//input[@data-field='username']")
element.send_keys("testuser")
```

Robo Appian approach:
```python
InputUtils.setValueByLabelText(wait, "Username", "testuser")
```

**Benefits:**
- More readable and maintainable
- Resilient to UI changes
- Business-user friendly

### 2. **Component-Specific Methods**

Each UI component type has dedicated utilities:

| Component Type | Utility Class | Purpose |
|----------------|---------------|---------|
| Text Inputs | `InputUtils` | Handle text fields, text areas |
| Buttons | `ButtonUtils` | Button interactions |
| Dropdowns | `DropdownUtils` | Dropdown selections |
| Date Pickers | `DateUtils` | Date input handling |
| Tables | `TableUtils` | Data table operations |
| Tabs | `TabUtils` | Tab navigation |

### 3. **Progressive Complexity**

Start simple and add complexity as needed:

```python
# Simple: Direct component interaction
ButtonUtils.clickByLabelText(wait, "Submit")

# Advanced: Data-driven with ComponentDriver
ComponentDriver.execute(wait, "Button", "Click", "Submit", None)

# Complex: Custom validation and error handling
try:
    ButtonUtils.clickByLabelText(wait, "Submit")
    if ComponentUtils.checkComponentExistsByXpath(wait, "//div[@class='success']"):
        logger.info("Submission successful")
except Exception as e:
    logger.error(f"Submission failed: {e}")
    take_screenshot("submission_error")
```

## Common Use Cases

### 1. **Form Automation**
Filling out Appian forms with various field types:

```python
def fill_employee_form(employee_data):
    """Fill out employee form with provided data"""
    InputUtils.setValueByLabelText(wait, "First Name", employee_data["first_name"])
    InputUtils.setValueByLabelText(wait, "Last Name", employee_data["last_name"])
    DateUtils.setValueByLabelText(wait, "Birth Date", employee_data["birth_date"])
    DropdownUtils.selectDropdownValueByLabelText(wait, "Department", employee_data["department"])
    ButtonUtils.clickByLabelText(wait, "Save Employee")
```

### 2. **Data Validation**
Verifying data in tables and forms:

```python
def validate_employee_data(expected_employee):
    """Validate employee appears in the table correctly"""
    table = TableUtils.findTableByColumnName(wait, "Employee ID")
    row_count = TableUtils.rowCount(table)
    
    for row in range(1, row_count + 1):
        emp_id = TableUtils.findComponentFromTableCell(wait, row, "Employee ID").text
        if emp_id == expected_employee["id"]:
            name = TableUtils.findComponentFromTableCell(wait, row, "Name").text
            assert name == expected_employee["name"]
            return True
    
    raise AssertionError(f"Employee {expected_employee['id']} not found")
```

### 3. **Workflow Testing**
Testing complete business processes:

```python
def test_employee_onboarding_workflow():
    """Test complete employee onboarding process"""
    # Login
    login_as_hr_manager()
    
    # Create employee
    create_new_employee(test_employee_data)
    
    # Assign to department
    assign_employee_to_department(test_employee_data["id"], "Engineering")
    
    # Set up benefits
    configure_employee_benefits(test_employee_data["id"])
    
    # Verify completion
    verify_employee_onboarding_complete(test_employee_data["id"])
```

## Integration Patterns

### With Testing Frameworks

Robo Appian integrates seamlessly with popular testing frameworks:

=== "pytest"
    ```python
    import pytest
    from selenium import webdriver
    from selenium.webdriver.support.ui import WebDriverWait
    
    @pytest.fixture(scope="session")
    def driver():
        driver = webdriver.Chrome()
        yield driver
        driver.quit()
    
    @pytest.fixture
    def wait(driver):
        return WebDriverWait(driver, 10)
    
    def test_login(driver, wait):
        driver.get("https://your-appian-app.com")
        InputUtils.setValueByLabelText(wait, "Username", "testuser")
        ButtonUtils.clickByLabelText(wait, "Sign In")
    ```

=== "unittest"
    ```python
    import unittest
    from selenium import webdriver
    from selenium.webdriver.support.ui import WebDriverWait
    
    class TestAppianUI(unittest.TestCase):
        def setUp(self):
            self.driver = webdriver.Chrome()
            self.wait = WebDriverWait(self.driver, 10)
        
        def tearDown(self):
            self.driver.quit()
        
        def test_form_submission(self):
            self.driver.get("https://your-appian-app.com")
            InputUtils.setValueByLabelText(self.wait, "Name", "Test")
            ButtonUtils.clickByLabelText(self.wait, "Submit")
    ```

## Next Steps



Ready to dive deeper? Choose your path:

<div class="grid cards" markdown>

-   <img src="https://raw.githubusercontent.com/Templarian/MaterialDesign/master/svg/cog.svg" alt="Start with Components" width="36" height="36" style="vertical-align:middle;"/>  
    **[Start with Components](components.md)**  
    Learn each component utility in detail  
    [:material-arrow-right: Core Components](components.md)

-   <img src="https://raw.githubusercontent.com/Templarian/MaterialDesign/master/svg/rocket-launch.svg" alt="Explore Advanced Features" width="36" height="36" style="vertical-align:middle;"/>  
    **[Explore Advanced Features](advanced.md)**  
    Discover powerful automation patterns  
    [:material-arrow-right: Advanced Features](advanced.md)

-   <img src="https://raw.githubusercontent.com/Templarian/MaterialDesign/master/svg/file-document-multiple.svg" alt="See Real Examples" width="36" height="36" style="vertical-align:middle;"/>  
    **[See Real Examples](../examples/login.md)**  
    Study complete test examples  
    [:material-arrow-right: Examples](../examples/login.md)

-   <img src="https://raw.githubusercontent.com/Templarian/MaterialDesign/master/svg/lifebuoy.svg" alt="Get Help" width="36" height="36" style="vertical-align:middle;"/>  
    **[Get Help](error-handling.md)**  
    Find answers to common questions  
    [:material-arrow-right: Error Handling](error-handling.md)

</div>

Happy testing with Robo Appian! 🚀
