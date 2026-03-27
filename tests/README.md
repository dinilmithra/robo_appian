# Tests Harness (pytest)

This folder contains a minimal pytest harness showing recommended usage patterns for `robo_appian` with Playwright.

## Fixtures
- `browser`: Session-scoped Playwright browser (`chromium` by default).
- `page`: Function-scoped Playwright page to follow the library's page-first pattern.
- `app_url`: Base URL from `APP_URL`; tests skip if unset.

## Example e2e Test
- `test_example_e2e.py` demonstrates both direct utility usage (for example, `InputUtils`, `ButtonUtils`) and orchestration via `ComponentDriver.execute()`.
- The test is marked `@pytest.mark.e2e` and is skipped unless explicitly enabled.

## Run Locally
Set environment and run pytest. Example (Windows PowerShell):

```powershell
# Install dependencies (Poetry)
poetry install

# Install Playwright browser binaries (one-time)
poetry run playwright install

# Optional: run in headless mode (default is 1)
$env:HEADLESS = "1"

# Required: enable e2e and provide your application URL
$env:RUN_E2E = "1"
$env:APP_URL = "https://your-appian-app.example.com/path"

# Optional: tweak timeouts
$env:PLAYWRIGHT_TIMEOUT_MS = "20000"

# Run only e2e-marked tests
poetry run pytest -m e2e -q

# Or run full suite (most will be skipped unless configured)
poetry run pytest -q
```

## Notes
- Playwright >= 1.52.0 is required (already declared in `pyproject.toml`).
- Adjust labels in the example test (e.g., `"Username"`, `"Sign In"`, `"Welcome"`) to match your Appian environment.
- Follow the library's conventions: pass `page` first to utilities.
