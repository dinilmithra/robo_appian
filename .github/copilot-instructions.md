# AI Coding Agent Instructions for robo_appian

These notes make AI agents productive quickly in this repo. They capture the patterns actually used here.

## Big Picture
- Purpose: Selenium helper library to automate Appian UI with readable, label-driven APIs.
- Structure: Static component utilities under [robo_appian/components](../robo_appian/components), shared helpers in [robo_appian/utils](../robo_appian/utils), high-level router in [robo_appian/controllers/ComponentDriver.py](../robo_appian/controllers/ComponentDriver.py).
- Style: Public APIs take `wait: WebDriverWait` first and derive `driver` via `wait._driver`. XPaths favor label text and ARIA patterns matching Appian DOM.

## Core Patterns
- Wait-first: Keep the `wait`-first signature; avoid exposing raw drivers (see [ComponentUtils.py](../robo_appian/utils/ComponentUtils.py)).
- Static utilities: Methods live as `@staticmethod`s on `*Utils` classes (Input, Button, Date, Dropdown, Search, Tab, Link, Label, Table).
- Safe clicks: Use `ComponentUtils.click(wait, el)` (ActionChains + clickable wait) instead of `el.click()`.
- Label-first selectors: Normalize whitespace + NBSP via `normalize-space(translate(., "\u00a0", " "))`; prefer label/abbr-driven XPaths over IDs.
- Visibility rules: Many locators exclude hidden nodes with `not(ancestor::*[@aria-hidden="true"])`; keep that guard when adding locators.
- Tables: Columns resolved from header `abbr` + class/id parsing; public APIs take 0-based rows (see [TableUtils.py](../robo_appian/components/TableUtils.py)).

## Component Usage (mirrors existing APIs)
- Inputs: `InputUtils.setValueByLabelText(wait, "Username", "test")` or partial label variants.
- Buttons: `ButtonUtils.clickByLabelText(wait, "Submit")` or partial label variants.
- Dates: `DateUtils.setValueByLabelText(wait, "Start Date", "01/01/2024")`.
- Dropdowns: `DropdownUtils.selectDropdownValueByLabelText(wait, "Status", "Active")` (combobox aria-controls pattern).
- Search dropdowns/inputs: Type then select using `*_searchInput` / `*_list` IDs (see SearchDropdownUtils/SearchInputUtils).
- Tabs/Links/Labels: Use visible text matchers (TabUtils/LinkUtils/LabelUtils).

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
- Tests: `pytest` available; tests may live externally—keep APIs deterministic/importable. Sample tests in [tests](../tests).
- Docs: `poetry run mkdocs serve` for local docs.
- Build/publish: `poetry build` (upload with twine as needed).
- CI helpers: Use [validate_simple.py](../validate_simple.py) or [validate_workflow.py](../validate_workflow.py) when touching `.github/workflows/*`.

## Gotchas
- Keep public APIs `wait`-first; if a raw driver is needed, hide it internally.
- Preserve NBSP normalization and hidden-element filters in new XPaths.
- Table APIs expect 0-based rows externally; adjust internally as in TableUtils.
- Search components rely on `aria-controls`/ID suffixes (`_searchInput`, `_list`, `_value`); follow those patterns when extending.

If anything is unclear or missing for your task (e.g., adding a new component utility or action type), ask for a quick clarification before proceeding.