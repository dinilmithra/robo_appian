# Architecture Overview

Robo Appian wraps Playwright with Appian-specific patterns, making tests business-readable and maintainable.

## Core Design Principles

### Page-First Pattern

Every robo_appian method accepts `page` as the first parameter. This ensures:

- Consistent timeout behavior across all interactions
- Automatic waiting for elements to be present, visible, and interactable
- No need for manual `time.sleep()` or custom wait logic
- Centralized timeout configuration (set once on the Playwright page/context)

```python
from playwright.sync_api import sync_playwright
from robo_appian.components import InputUtils, ButtonUtils

with sync_playwright() as playwright:
    browser = playwright.chromium.launch()
    page = browser.new_page()
    page.set_default_timeout(10_000)
    page.goto("https://your-appian.example.com")

    InputUtils.setValueByLabelText(page, "Username", "test_user")
    ButtonUtils.clickByLabelText(page, "Sign In")
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

- **Locator visibility checks**: Waits until the target is interactable
- **Scroll into view**: Reduces viewport-related click failures
- **Playwright click handling**: Uses locator-based clicks with the shared timeout
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
- Keeps the Playwright wrappers small and composable

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
    ButtonUtils.clickByLabelText(page, "Load More")

RoboUtils.retry_on_timeout(flaky_operation, max_retries=3, operation_name="Load More Click")
```

This handles:

- Temporary network delays
- Animation timing issues
- Sporadic stale element references

### Partial Label Matching

When Appian appends dynamic text to labels (e.g., "Username (Production)" vs "Username (Test)"), use partial matching:

```python
InputUtils.setValueByPartialLabelText(page, "Username", "test_user")
```

This matches any label containing "Username", making tests environment-agnostic.

## When to Use Robo Appian

**Ideal for:**
- Appian UI regression and end-to-end testing
- CI/CD automation pipelines
- Data-driven test scenarios

**Not recommended for:**
- Non-Appian applications
- API testing

See [Components](components.md) for detailed usage patterns.
