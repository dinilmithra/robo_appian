# Advanced Features

## Routing With ComponentDriver

Use `ComponentDriver.execute(page, type, action, label, value)` when your tests are driven by tables, spreadsheets, or reusable step definitions.

Supported combinations include:
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

## Retry Flaky Actions

Wrap known timeout-prone actions with `RoboUtils.retry_on_timeout(...)` instead of adding global sleeps.
