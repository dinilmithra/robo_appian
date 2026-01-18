# Best Practices

- **Always pass `wait` first**: Public APIs accept `WebDriverWait` then derive `driver` via `wait._driver`. Keep custom helpers consistent.
- **Normalize labels**: Use exact label APIs when possible; fall back to partial label variants when labels carry dynamic counts/suffixes.
- **Keep NBSP handling**: Locators rely on `translate(., "\u00a0", " ")` to normalize Appian whitespace—preserve this in new XPaths.
- **Use safe click**: Prefer `ComponentUtils.click` over `element.click()` to handle overlays/animations.
- **Respect table indexing**: Public table APIs take 0-based rows; convert to 1-based only inside helpers.
- **Retry intentionally**: Wrap only flaky waits/actions with `RoboUtils.retry_on_timeout`; avoid masking real failures.
- **Keep APIs deterministic**: Avoid global state; ensure utilities are importable and side-effect free for external tests.
