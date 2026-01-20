# AI Coding Agent Instructions for robo_appian

These notes make AI agents productive quickly in this repo. They capture the patterns actually used here.

## Big Picture
- Purpose: Selenium helper library to automate Appian UI with readable, label-driven APIs.
- Structure: Static component utilities under [robo_appian/components](../robo_appian/components), shared helpers in [robo_appian/utils](../robo_appian/utils), high-level router in [robo_appian/controllers/ComponentDriver.py](../robo_appian/controllers/ComponentDriver.py).
- Style: Public APIs take `wait: WebDriverWait` first and derive `driver` via `wait._driver`. XPaths favor label text and ARIA patterns matching Appian DOM.
- Testing: Sample pytest harness in [tests](../tests) with fixtures for driver/wait; production tests may live in consumer repos.

## Core Patterns
- **Wait-first signature**: All public methods take `wait: WebDriverWait` as first param; derive driver internally via `wait._driver`.
- **Static utilities**: Methods live as `@staticmethod`s on `*Utils` classes (Input, Button, Date, Dropdown, Search, Tab, Link, Label, Table, Browser).
- **Safe clicks**: Use `ComponentUtils.click(wait, el)` (ActionChains + element_to_be_clickable) instead of `el.click()` to handle overlays/animations.
- **Label-first selectors**: Normalize whitespace + NBSP via `normalize-space(translate(., "\u00a0", " "))`; prefer label/abbr-driven XPaths over IDs.
- **Visibility rules**: Many locators exclude hidden nodes with `not(ancestor::*[@aria-hidden="true"])` or `not(ancestor-or-self::*[contains(@class, "---hidden")])`; preserve these guards.
- **Tables**: Columns resolved from header `abbr` + class/id parsing; public APIs take 0-based rows, internally convert to 1-based `data-dnd-name="row {n+1}"` (see [TableUtils.py](../robo_appian/components/TableUtils.py)).

## Component API Patterns
All utilities follow consistent naming: `*ByLabelText` (exact match), `*ByPartialLabelText`, `*ById`, `*ByPlaceholderText` where applicable.

- **Inputs**: `InputUtils.setValueByLabelText(wait, "Username", "test")` clears field then types via ActionChains.
- **Buttons**: `ButtonUtils.clickByLabelText(wait, "Submit")` uses safe click; `isButtonExistsByLabelText` for checks.
- **Dates**: `DateUtils.setValueByLabelText(wait, "Start Date", "01/01/2024")` expects MM/DD/YYYY format.
- **Dropdowns**: `DropdownUtils.selectDropdownValueByLabelText(wait, "Status", "Active")` uses combobox `aria-controls` pattern; finds combobox → clicks → locates list by ID → selects option.
- **Search components**: SearchDropdownUtils/SearchInputUtils type then select from `*_searchInput` / `*_list` ID suffixes.
- **Tabs/Links/Labels**: TabUtils/LinkUtils/LabelUtils match visible text; TabUtils checks `aria-selected` state.
- **Tables**: `TableUtils.findTableByColumnName(wait, "Employee ID")` → `rowCount(table)` → `selectRowFromTableByColumnNameAndRowNumber(wait, 0, col)` (0-based rows).
- **Browser**: BrowserUtils manages tabs—`switch_to_Tab(wait, idx)`, `switch_to_next_tab(wait)`, `close_current_tab_and_switch_back(wait)`.

## Routing Actions
- Use `ComponentDriver.execute(wait, type, action, label, value)` as the orchestration entrypoint.
  - Examples: `( "Date", "Set Value", label, value )`, `( "Button", "Click", label, None )`, `( "Drop Down", "Select", label, value )`.
  - When adding a new utility, wire precise `type`/`action` strings into the `match` blocks.

## Resilience & Helpers
- Retry: Wrap flaky waits/actions with `RoboUtils.retry_on_timeout(op, max_retries, name)`.
- Element access: Prefer `ComponentUtils.waitForComponentToBeVisibleByXpath` and siblings for consistent waits/diagnostics.
- Version helper: `ComponentUtils.get_version()` reads `pyproject.toml`; keep file location stable.

## Dev Workflows
- Python 3.12; Selenium >= 4.34.0 (see [pyproject.toml](../pyproject.toml)).
- Install for dev:
  ```bash
  pip install -r requirements.txt
  poetry install
  ```
- **Tests**: pytest harness in [tests](../tests); fixtures: `driver` (session Chrome via Selenium Manager), `wait` (function-scoped), `app_url` (from `APP_URL` env).
  ```powershell
  # Run e2e tests (Windows PowerShell)
  $env:RUN_E2E = "1"
  $env:APP_URL = "https://your-appian-app.example.com"
  $env:HEADLESS = "1"  # Optional: default is headless
  $env:SELENIUM_WAIT_TIMEOUT = "15"  # Optional: default 15s
  poetry run pytest -m e2e -v
  ```
- **Docs**: `poetry run mkdocs serve` for local preview; `mkdocs build` generates [site](../site). MkDocs Material theme with API autodoc via mkdocstrings.
- **Build/publish**: `poetry build` creates wheel/sdist in `dist/`; publish to PyPI via `twine upload dist/*` or CI.
- **CI validation**: Use [validate_simple.py](../validate_simple.py) or [validate_workflow.py](../validate_workflow.py) when editing `.github/workflows/*.yml`—these check YAML validity, required fields, deprecated actions.

## Gotchas
- Keep public APIs `wait`-first; if a raw driver is needed, hide it internally.
- Preserve NBSP normalization and hidden-element filters in new XPaths.
- Table APIs expect 0-based rows externally; adjust internally as in TableUtils.
- Search components rely on `aria-controls`/ID suffixes (`_searchInput`, `_list`, `_value`); follow those patterns when extending.

If anything is unclear or missing for your task (e.g., adding a new component utility or action type), ask for a quick clarification before proceeding.