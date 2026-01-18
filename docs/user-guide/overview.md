# Overview

Robo Appian is a Python library that transforms Appian UI test automation by providing label-driven, readable APIs built on top of Selenium WebDriver. Instead of maintaining brittle XPath selectors or element IDs that break with every Appian update, Robo Appian leverages the visible labels and ARIA attributes that business users already see on screen.

## What is Robo Appian?

Robo Appian wraps Selenium with Appian-specific locators and patterns so tests read like business steps. Every public API uses a `WebDriverWait` first, automatically derives the driver via `wait._driver`, and relies on label/ARIA metadata to find elements. This approach makes tests:

- **Business-readable**: Use the same terms your product owners use ("Click Submit", "Set Username to test_user")
- **Resilient**: Labels rarely change; internal IDs and structure shift constantly
- **Maintainable**: One line of code replaces complex XPath and wait logic
- **Self-documenting**: Method names describe intent, not implementation

## Core Design Principles

### Wait-First Pattern

Every robo_appian method accepts `WebDriverWait` as the first parameter. This ensures:

- Consistent timeout behavior across all interactions
- Automatic waiting for elements to be present, visible, and interactable
- No need for manual `time.sleep()` or custom wait logic
- Centralized timeout configuration (set once when creating `WebDriverWait`)

```python
from selenium.webdriver.support.ui import WebDriverWait

# Configure wait once
wait = WebDriverWait(driver, 10)

# All methods use this wait automatically
InputUtils.setValueByLabelText(wait, "Username", "test_user")
ButtonUtils.clickByLabelText(wait, "Sign In")
```

### Label-Driven Selectors

Robo Appian locates elements by their visible labels—the text users actually see. This is powered by:

- **Label-to-input associations**: HTML `<label for="...">` attributes that connect labels to form fields
- **ARIA attributes**: `aria-label`, `aria-labelledby`, and `aria-controls` for complex components
- **Header abbreviations**: Table columns identified by `abbr` attributes on headers
- **Normalized text matching**: Automatic handling of whitespace and non-breaking spaces (NBSP)

### Safe Click Operations

Direct `element.click()` calls fail frequently due to:

- Elements covered by overlays or animations
- Timing issues during page transitions
- Stale element references after DOM updates

Robo Appian's `ComponentUtils.click()` method combines:

- **Explicit wait**: Ensures element is clickable before interaction
- **ActionChains**: Moves mouse to element center and performs reliable click
- **Error context**: Provides clear diagnostics when clicks fail

All robo_appian click operations use this safe pattern internally.

## Library Structure

### Component Utilities

Located in `robo_appian/components`, these static utility classes handle specific Appian UI elements:

- **ButtonUtils**: Click buttons by label text (exact or partial matching)
- **InputUtils**: Fill text inputs by label or placeholder
- **DateUtils**: Set date picker values by label
- **DropdownUtils**: Select from standard dropdowns (aria-controls pattern)
- **SearchDropdownUtils**: Type and select from filterable dropdowns
- **SearchInputUtils**: Interact with searchable input fields
- **TableUtils**: Find tables, count rows, click cells, extract data
- **TabUtils**: Navigate between tab panels
- **LabelUtils**: Verify label existence and visibility
- **LinkUtils**: Click links by visible text

Each utility provides multiple methods for common variations (exact label, partial label, by ID, by placeholder, etc.).

### Shared Utilities

Located in `robo_appian/utils`, these provide foundational capabilities:

- **ComponentUtils**: Core element finding, waiting, clicking, and version utilities
- **RoboUtils**: Retry logic for flaky operations (`retry_on_timeout`)
- **BrowserUtils**: Browser management and configuration helpers

## Key Patterns

### Static Method Design

All component utilities are designed as static classes. This approach:

- Eliminates unnecessary object instantiation
- Makes imports cleaner (`from robo_appian.components import InputUtils`)
- Signals that methods are stateless and side-effect free
- Follows Selenium's established patterns

### Table Interactions

Tables are particularly complex in Appian. TableUtils provides:

- **Column identification**: Uses `abbr` attribute on `<th>` elements
- **Row indexing**: Public APIs use 0-based indexing; internally converts to Appian's 1-based `data-dnd-name` attribute
- **Cell navigation**: Finds components within specific cells by column name + row number
- **Data extraction**: Reads text from cells for assertions

### Version Management

`ComponentUtils.get_version()` reads the version from `pyproject.toml` at runtime, enabling:

- Dynamic version reporting in logs
- Version-aware debugging
- Compatibility checks in test setup

## Resilience Features

### Automatic Retries

`RoboUtils.retry_on_timeout()` wraps flaky operations:

```python
def flaky_operation():
    ButtonUtils.clickByLabelText(wait, "Load More")

RoboUtils.retry_on_timeout(flaky_operation, max_retries=3, name="Load More Click")
```

This handles:

- Temporary network delays
- Animation timing issues
- Sporadic stale element references

### Partial Label Matching

When Appian appends dynamic text to labels (e.g., "Username (Production)" vs "Username (Test)"), use partial matching:

```python
InputUtils.setValueByPartialLabelText(wait, "Username", "test_user")
```

This matches any label containing "Username", making tests environment-agnostic.

### Multiple Wait Strategies

Different methods provide appropriate wait conditions:

- `visibility_of_element_located`: For elements that must be visible
- `element_to_be_clickable`: For interactive elements
- `presence_of_element_located`: For DOM presence checks
- `invisibility_of_element_located`: For waiting until elements disappear

## Integration Patterns

### Pytest Integration

```python
import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

@pytest.fixture
def browser():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    yield driver, wait
    driver.quit()

def test_login(browser):
    driver, wait = browser
    driver.get("https://your-appian.example.com")
    InputUtils.setValueByLabelText(wait, "Username", "test_user")
    ButtonUtils.clickByLabelText(wait, "Sign In")
```

### Unittest Integration

```python
import unittest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

class AppianTests(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)
    
    def tearDown(self):
        self.driver.quit()
    
    def test_form_submission(self):
        self.driver.get("https://your-appian.example.com")
        InputUtils.setValueByLabelText(self.wait, "Title", "Test Request")
        ButtonUtils.clickByLabelText(self.wait, "Submit")
```

## When to Use Robo Appian

### Ideal Use Cases

- **Regression testing**: Verify existing functionality remains intact after Appian upgrades
- **End-to-end workflows**: Test complete business processes from login to data submission
- **Data-driven testing**: Run the same test flow with multiple data sets
- **CI/CD pipelines**: Automated testing before production deployments
- **Smoke testing**: Quickly verify critical paths after releases

### Not Recommended For

- **Non-Appian applications**: Library is optimized for Appian's DOM structure
- **API testing**: Use direct HTTP clients for backend API tests
- **Unit testing**: Test business logic separately from UI
- **Performance testing**: Use load testing tools (JMeter, Locust) instead

## Technical Requirements

- **Python**: 3.12 or higher (uses match/case syntax)
- **Selenium**: 4.34.0 or higher (modern WebDriver API)
- **Browser drivers**: ChromeDriver, GeckoDriver, etc. must be installed and in PATH

## Learning Path

1. **Installation & Setup**: Start with [Installation](../getting-started/installation.md)
2. **First Test**: Follow [Your First Test](../getting-started/first-test.md)
3. **Component Guide**: Read [Core Components](components.md) to understand each utility
4. **Examples**: Study real scenarios in [Examples](../examples/login.md)
5. **Advanced Features**: Explore [Advanced Features](advanced.md) for complex scenarios
6. **Best Practices**: Review [Best Practices](best-practices.md) for maintainable tests

Continue to [Components](components.md) for detailed component patterns and API documentation.
