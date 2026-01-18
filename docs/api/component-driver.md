# Component Driver

High-level router for data-driven automation.

## Method

### execute
```python
ComponentDriver.execute(wait, type, action, label, value)
```
Execute an action by component type and action string.

**Supported types/actions:**
- `("Input Text", "Set Value", label, value)`
- `("Button", "Click", label, None)`
- `("Drop Down", "Select", label, value)`
- `("Search Drop Down", "Select", label, value)`
- `("Search Input Text", "Select", label, value)`
- `("Date", "Set Value", label, value)`
- `("Tab", "Find", label, None)`
- `("Link", "Click", label, None)`
- `("Label", "Find", label, None)`