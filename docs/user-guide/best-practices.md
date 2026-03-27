# Best Practices

- Pass `page` first to every public robo_appian API.
- Prefer label-driven selectors over raw ids when possible.
- Escape user-provided XPath text with `ComponentUtils.xpath_literal(...)`.
- Reuse `ComponentUtils.click(page, locator)` instead of calling raw clicks from custom helpers.
- Keep table row numbers zero-based when calling `TableUtils` public methods.
- Use `RoboUtils.retry_on_timeout(...)` only for known transient waits.
