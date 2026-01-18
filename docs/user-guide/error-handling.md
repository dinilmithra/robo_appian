# Error Handling

## Common failures
- **TimeoutException**: Element not found/visible/clickable within `WebDriverWait`. Verify labels match exactly and the component is not hidden or disabled.
- **ValueError**: Label missing a `for` attribute (inputs/dates) or combobox missing `aria-controls`. Inspect the page markup and adjust the locator.
- **StaleElementReference**: DOM refreshed between lookup and interaction. Re-query via the util rather than reusing stale elements.

## Debug tips
- Increase wait duration temporarily during investigation.
- Use `ComponentUtils.waitForComponentToBeVisibleByXpath` with a narrowed XPath to confirm visibility.
- For dropdowns/search inputs, check the derived IDs: `*_searchInput`, `*_list`, `*_value`.
- For tables, confirm the header `abbr` matches the column name you pass.

## Recovery patterns
- Wrap flaky operations with `RoboUtils.retry_on_timeout` to reattempt timeouts.
- For dependent steps, wait for negative conditions (e.g., `waitForComponentNotToBeVisibleByXpath`) before proceeding to avoid overlay issues.
