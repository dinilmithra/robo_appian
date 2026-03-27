# Component Utils

`ComponentUtils` provides shared Playwright helpers used across the library.

## Common Methods
- `click(page, component)`: Scroll into view and click a locator safely.
- `waitForComponentToBeVisibleByXpath(page, xpath)`: Wait for a visible XPath match.
- `waitForComponentNotToBeVisibleByXpath(page, xpath)`: Wait for a hidden XPath match.
- `findComponentById(page, id)`: Find a visible element by id.
- `findComponentsByXPath(page, xpath)`: Collect visible, enabled matches.
- `retry_until(...)`: Retry a callable until it succeeds or times out.
- `xpath_literal(value)`: Escape user-provided text before inserting it into XPath.
- `today()` / `yesterday()`: Convenience date helpers in `MM/DD/YYYY` format.

## Example
```python
text = ComponentUtils.xpath_literal("Manager's Approval")
locator = ComponentUtils.waitForComponentToBeVisibleByXpath(
    page,
    f"//span[normalize-space(translate(., '\u00a0', ' '))={text}]",
)
ComponentUtils.click(page, locator)
```
