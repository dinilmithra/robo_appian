# Advanced Features

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
