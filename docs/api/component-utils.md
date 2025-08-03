# ComponentUtils API Reference

The `ComponentUtils` class provides fundamental utilities for component interaction, date operations, and element validation in Robo Appian.

## Import

```python
from robo_appian.utils.ComponentUtils import ComponentUtils
```

## Date Utilities

### today()

Returns today's date formatted as MM/DD/YYYY.

**Returns:**
- `str`: Today's date in MM/DD/YYYY format

**Example:**
```python
today_date = ComponentUtils.today()
print(f"Today's date: {today_date}")  # Output: Today's date: 08/03/2025
```

---

### yesterday()

Returns yesterday's date formatted as MM/DD/YYYY.

**Returns:**
- `str`: Yesterday's date in MM/DD/YYYY format

**Example:**
```python
yesterday_date = ComponentUtils.yesterday()
print(f"Yesterday's date: {yesterday_date}")  # Output: Yesterday's date: 08/02/2025
```

## Component Location Methods

### findComponentUsingXpath(wait, xpath)

Finds a component using the given XPath in the current WebDriver instance.

**Parameters:**
- `wait` (WebDriverWait): WebDriverWait instance to wait for elements
- `xpath` (str): XPath string to locate the component

**Returns:**
- `WebElement`: The located WebElement

**Raises:**
- `NoSuchElementException`: If the element is not found

**Example:**
```python
component = ComponentUtils.findComponentUsingXpath(wait, "//button[@id='submit']")
component.click()
```

---

### findComponentUsingXpathAndClick(wait, xpath)

Finds a component using the given XPath and clicks it.

**Parameters:**
- `wait` (WebDriverWait): WebDriverWait instance to wait for elements
- `xpath` (str): XPath string to locate the component

**Returns:**
- `None`

**Example:**
```python
ComponentUtils.findComponentUsingXpathAndClick(wait, "//button[@id='submit']")
```

---

### findChildComponent(wait, component, xpath)

Finds a child component using the given XPath within a parent component.

**Parameters:**
- `wait` (WebDriverWait): WebDriverWait instance to wait for elements
- `component` (WebElement): Parent WebElement to search within
- `xpath` (str): XPath string to locate the child component

**Returns:**
- `WebElement`: The located child WebElement

**Example:**
```python
parent_component = driver.find_element(By.ID, "parent")
child_component = ComponentUtils.findChildComponent(wait, parent_component, ".//button[@class='child']")
```

---

### findComponentsByXPath(wait, xpath)

Finds all components matching the given XPath and returns a list of valid components that are clickable and displayed.

**Parameters:**
- `wait` (WebDriverWait): WebDriverWait instance to wait for elements
- `xpath` (str): XPath string to locate components

**Returns:**
- `List[WebElement]`: List of valid WebElement components

**Raises:**
- `Exception`: If no valid components are found

**Example:**
```python
components = ComponentUtils.findComponentsByXPath(wait, "//button[@class='submit']")
for component in components:
    component.click()
```

## Validation Methods

### checkComponentExistsByXpath(wait, xpath)

Checks if a component with the given XPath exists in the current WebDriver instance.

**Parameters:**
- `wait` (WebDriverWait): WebDriverWait instance to wait for elements
- `xpath` (str): XPath string to locate the component

**Returns:**
- `bool`: True if the component exists, False otherwise

**Example:**
```python
if ComponentUtils.checkComponentExistsByXpath(wait, "//div[@id='success-message']"):
    print("Success message found!")
else:
    print("Success message not found!")
```

---

### checkComponentExistsById(driver, id)

Checks if a component with the given ID exists in the current WebDriver instance.

**Parameters:**
- `driver` (WebDriver): WebDriver instance to check for the component
- `id` (str): ID of the component to check

**Returns:**
- `bool`: True if the component exists, False otherwise

**Example:**
```python
exists = ComponentUtils.checkComponentExistsById(driver, "submit-button")
print(f"Component exists: {exists}")
```

---

### findCount(wait, xpath)

Finds the count of components matching the given XPath.

**Parameters:**
- `wait` (WebDriverWait): WebDriverWait instance to wait for elements
- `xpath` (str): XPath string to locate components

**Returns:**
- `int`: Count of components matching the XPath

**Example:**
```python
count = ComponentUtils.findCount(wait, "//div[@class='item']")
print(f"Number of items found: {count}")
```

## Utility Methods

### tab(wait)

Simulates a tab key press in the current WebDriver instance.

**Parameters:**
- `wait` (WebDriverWait): WebDriverWait instance to wait for elements

**Returns:**
- `None`

**Example:**
```python
ComponentUtils.tab(wait)  # Presses Tab key
```

## Complete Usage Example

```python
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from robo_appian.utils.ComponentUtils import ComponentUtils

def test_component_utils():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    
    try:
        driver.get("https://example.com")
        
        # Get today's date for form filling
        today = ComponentUtils.today()
        yesterday = ComponentUtils.yesterday()
        print(f"Today: {today}, Yesterday: {yesterday}")
        
        # Check if a component exists before interacting
        if ComponentUtils.checkComponentExistsByXpath(wait, "//input[@id='date-field']"):
            date_field = ComponentUtils.findComponentUsingXpath(wait, "//input[@id='date-field']")
            date_field.send_keys(today)
        
        # Count how many buttons are on the page
        button_count = ComponentUtils.findCount(wait, "//button")
        print(f"Found {button_count} buttons on the page")
        
        # Find and click all submit buttons
        submit_buttons = ComponentUtils.findComponentsByXPath(wait, "//button[contains(@class, 'submit')]")
        for button in submit_buttons:
            button.click()
        
        # Use tab to navigate
        ComponentUtils.tab(wait)
        
        # Check if operation was successful
        if ComponentUtils.checkComponentExistsByXpath(wait, "//div[@class='success']"):
            print("Operation completed successfully!")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    test_component_utils()
```

## Related Components

- [ButtonUtils](button-utils.md) - For button-specific operations
- [InputUtils](input-utils.md) - For input field operations
- [TableUtils](table-utils.md) - For table operations

::: robo_appian.utils.ComponentUtils
