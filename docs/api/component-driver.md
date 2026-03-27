# Component Driver

`ComponentDriver` is the high-level router for data-driven Playwright flows.

## Method

```python
ComponentDriver.execute(page, type, action, label, value)
```

## Supported Routes

- `( "Input Text", "Set Value", label, value )`
- `( "Button", "Click", label, None )`
- `( "Drop Down", "Select", label, value )`
- `( "Search Drop Down", "Select", label, value )`
- `( "Search Input Text", "Select", label, value )`
- `( "Date", "Set Value", label, value )`
- `( "Tab", "Find", label, None )`
- `( "Tab", "Click", label, None )`
- `( "Link", "Click", label, None )`
- `( "Label", "Find", label, None )`

Unsupported combinations raise `MyCustomError`.

## Example

```python
from robo_appian.controllers.ComponentDriver import ComponentDriver

steps = [
	("Input Text", "Set Value", "Username", "demo_user"),
	("Button", "Click", "Sign In", None),
]

for type_, action, label, value in steps:
	ComponentDriver.execute(page, type_, action, label, value)
```
