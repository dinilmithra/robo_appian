# ComponentDriver API Reference

The `ComponentDriver` class provides a unified interface for executing actions on various component types using a single method call. This utility simplifies automation scripts by providing a consistent API across different Appian UI components.

## Import

```python
from robo_appian.controllers.ComponentDriver import ComponentDriver
```

## Universal Execute Method

### execute()

Executes actions on any supported component type using a unified interface.

**Syntax:**
```python
ComponentDriver.execute(wait, component_type, action, label, value)
```

**Parameters:**
- `wait` (WebDriverWait): Selenium WebDriverWait instance
- `component_type` (str): Type of component to interact with
- `action` (str): Action to perform on the component
- `label` (str): Label text to identify the component
- `value` (str|None): Value to set (None for click actions)

**Returns:**
- Result varies by component type and action

## Supported Components

### Date Components

Handle date picker and date input components.

**Component Type:** `"Date"`  
**Supported Actions:** `"Set Value"`

```python
ComponentDriver.execute(wait, "Date", "Set Value", "Start Date", "01/15/2024")
```

### Input Text Components

Handle standard text input fields, text areas, and password fields.

**Component Type:** `"Input Text"`  
**Supported Actions:** `"Set Value"`

```python
ComponentDriver.execute(wait, "Input Text", "Set Value", "First Name", "John")
```

### Dropdown Components

Handle standard dropdown/select components.

**Component Type:** `"Dropdown"`  
**Supported Actions:** `"Select"`

```python
ComponentDriver.execute(wait, "Dropdown", "Select", "Department", "Engineering")
```

### Button Components

Handle button elements for actions like submit, save, etc.

**Component Type:** `"Button"`  
**Supported Actions:** `"Click"`

```python
ComponentDriver.execute(wait, "Button", "Click", "Save Employee", None)
```

### Tab Components

Handle tab navigation in multi-step forms.

**Component Type:** `"Tab"`  
**Supported Actions:** `"Click"`

```python
ComponentDriver.execute(wait, "Tab", "Click", "Personal Information", None)
```

## Example Usage

```python
from selenium.webdriver.support.ui import WebDriverWait
from robo_appian.controllers.ComponentDriver import ComponentDriver

wait = WebDriverWait(driver, 10)
ComponentDriver.execute(wait, "Input Text", "Set Value", "Username", "john.doe")
ComponentDriver.execute(wait, "Button", "Click", "Login", None)
```

## See Also
- [DropdownUtils](dropdown-utils.md)
- [ButtonUtils](button-utils.md)
- [TabUtils](tab-utils.md)
