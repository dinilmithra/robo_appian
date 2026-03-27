# Error Handling

## Common Failures
- `Playwright TimeoutError`: The target element did not become visible, hidden, or clickable before the configured timeout.
- `ValueError`: A helper could not resolve a required id, aria attribute, or table column index.
- `MyCustomError`: `ComponentDriver` received an unsupported component/action pair or a required value was missing.

## Practical Checks
- Confirm the visible label text matches the Appian UI exactly.
- Verify the component is not inside an `aria-hidden` container.
- For dropdown and search components, confirm the Appian `aria-controls` relationship is present.
- For tables, verify the target column header has the expected `abbr` value.
