
# Robo Appian: A Python Library for Appian UI Test Automation

In response to the growing need for robust and streamlined testing of Appian applications, we are proud to introduce robo_appian, a powerful open-source Python library designed to simplify and accelerate the creation of automated test scripts for Appian user interfaces. This library provides a high-level API to interact with Appian's unique UI components, abstracting away the complexities of their underlying implementation and enabling developers and QA engineers to write more readable, maintainable, and resilient tests.

robo_appian is built on top of the widely-used Selenium WebDriver framework, allowing for cross-browser testing and seamless integration into existing testing workflows. It addresses the common challenge of locating and interacting with Appian's dynamically generated UI elements by providing a set of intuitive functions and locator strategies tailored specifically for the Appian platform.

## Why use Robo Appian?

- **Simplified Component Interaction:** The library offers a suite of functions for easily finding and manipulating common Appian UI components such as text fields, buttons, dropdowns, grids, and more.

- **Robust Locator Strategies:** appian-automator employs intelligent locator strategies that go beyond simple ID or class name matching, making tests less brittle and more resistant to changes in the application's UI.

- **Improved Readability and Maintainability:** By providing a higher-level of abstraction, the library allows for the creation of test scripts that are more descriptive and easier to understand, reducing the maintenance overhead.

- **Seamless Selenium Integration:** Built as a layer on top of Selenium, appian-automator allows users to leverage the full power and flexibility of the Selenium framework when needed.

- **Extensibility:** The library is designed to be extensible, allowing users to add custom functions and locator strategies for unique or complex UI components.

## Quick Start Example
```python
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from robo_appian.components.InputUtils import InputUtils
from robo_appian.components.ButtonUtils import ButtonUtils

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)
driver.get("https://your-appian-app.com")

InputUtils.setValueByLabelText(wait, "Username", "test_user")
InputUtils.setValueByLabelText(wait, "Password", "password123")
ButtonUtils.clickByLabelText(wait, "Sign In")
driver.quit()
```

## What can you automate?
- Text fields, dropdowns, buttons, dates, tables, tabs, and more

## Learn More
- [Quick Start Guide](getting-started/quick-start.md)
- [User Guide](user-guide/overview.md)
- [API Reference](api/component-utils.md)
- [Examples](examples/login.md)

## Main Components
| Component         | What it does                | Example Usage                                      |
|-------------------|----------------------------|----------------------------------------------------|
| ButtonUtils       | Click Appian buttons       | `ButtonUtils.clickByLabelText(wait, "Submit")`     |
| InputUtils        | Enter text in fields       | `InputUtils.setValueByLabelText(wait, "Name", "John")` |
| DropdownUtils     | Select dropdown options    | `DropdownUtils.selectDropdownValueByLabelText(wait, "Status", "Active")` |
| DateUtils         | Set date fields            | `DateUtils.setValueByLabelText(wait, "Start Date", "01/15/2024")` |
| TableUtils        | Work with data tables      | `TableUtils.findTableByColumnName(wait, "Employee ID")` |
| ComponentDriver   | Universal component action | `ComponentDriver.execute(wait, "Input Text", "Set Value", "Name", "John")` |

## Author
**Dinil Mithra**  
[LinkedIn](https://www.linkedin.com/in/dinilmithra) | dinilmithra.mailme@gmail.com

---
MIT License
