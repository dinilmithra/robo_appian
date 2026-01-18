# Advanced Features

## Routing with ComponentDriver
`ComponentDriver.execute(wait, type, action, label, value)` maps data-driven steps to the right util. Supported types/actions include:
- `("Input Text", "Set Value", label, value)`
- `("Button", "Click", label, None)`
- `("Drop Down", "Select", label, value)`
- `("Search Drop Down", "Select", label, value)`
- `("Search Input Text", "Select", label, value)`
- `("Date", "Set Value", label, value)`
- `("Tab", "Find", label, None)`
- `("Link", "Click", label, None)`
- `("Label", "Find", label, None)`

Add new component types by wiring the `match` blocks inside `ComponentDriver` to the appropriate util.

## Retrying flaky actions
Use `RoboUtils.retry_on_timeout(op, max_retries, name)` to wrap waits or actions that may intermittently time out.

```python
from robo_appian.utils.RoboUtils import RoboUtils
from robo_appian.components import ButtonUtils

RoboUtils.retry_on_timeout(
    lambda: ButtonUtils.clickByLabelText(wait, "Submit"),
    max_retries=3,
    operation_name="click submit",
)
```

## Safe clicking everywhere
All click paths funnel through `ComponentUtils.click(wait, element)`, which waits for clickability and uses ActionChains to bypass overlay/animation issues. Use it for any custom elements you locate yourself.

## Version helper
`ComponentUtils.get_version()` reads `pyproject.toml` from repo root—useful for diagnostics and reporting.
