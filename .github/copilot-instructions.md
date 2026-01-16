# AI Coding Agent Instructions for robo_appian

These notes make AI agents productive quickly in this repo. They document the actual patterns used here — not generic advice.

## Big Picture
- Purpose: A Selenium-based helper library to automate Appian UI via readable, label-driven APIs.
- Structure: Component-focused static utility classes under [robo_appian/components](../robo_appian/components), shared helpers in [robo_appian/utils](../robo_appian/utils), an action router in [robo_appian/controllers/ComponentDriver.py](../robo_appian/controllers/ComponentDriver.py).
- Style: All operations take a `WebDriverWait` (`wait`) and derive `driver` from `wait._driver`. XPaths prefer label text and ARIA attributes that match Appian’s DOM.

## Core Patterns (follow these)
- `WebDriverWait` first: All APIs accept `wait: WebDriverWait` as the first arg and internally use `wait._driver` (example: [ComponentUtils.py](../robo_appian/utils/ComponentUtils.py)). Avoid requiring raw `driver` in new public methods.
- Static utilities: Methods are `@staticmethod`s on `*Utils` classes (e.g., `InputUtils`, `ButtonUtils`). Keep additions consistent with this pattern.
- Safe clicking: Use `ComponentUtils.click(wait, el)` which waits for clickability and uses `ActionChains` instead of `el.click()` (see [ComponentUtils.py](../robo_appian/utils/ComponentUtils.py)).
- Label-first selectors: Prefer exact or partial label matching with normalized whitespace and NBSP handling using `normalize-space(translate(., "\u00a0", " "))` (examples in [InputUtils.py](../robo_appian/components/InputUtils.py) and [ButtonUtils.py](../robo_appian/components/ButtonUtils.py)).
- Visibility/hidden rules: Many XPaths exclude hidden nodes using `not(ancestor::*[@aria-hidden="true"])` or class checks (see [LinkUtils.py](../robo_appian/components/LinkUtils.py)). Preserve this when adding locators.
- Tables: Columns identified via header `abbr` and header class/id parsing; rows are 0-based in public APIs (see [TableUtils.py](../robo_appian/components/TableUtils.py)).

## Component Catalog (examples mirror existing usage)
- Inputs: `InputUtils.setValueByLabelText(wait, "Username", "test")` and `setValueByPartialLabelText` (see [InputUtils.py](../robo_appian/components/InputUtils.py)).
- Buttons: `ButtonUtils.clickByLabelText(wait, "Submit")` or partial label variants (see [ButtonUtils.py](../robo_appian/components/ButtonUtils.py)).
- Dates: `DateUtils.setValueByLabelText(wait, "Start Date", "01/01/2024")` (see [DateUtils.py](../robo_appian/components/DateUtils.py)).
- Dropdowns: Select by label; relies on ARIA combobox and list patterns (see [DropdownUtils.py](../robo_appian/components/DropdownUtils.py)).
- Search Dropdowns/Inputs: Type then pick from list using ID conventions `*_searchInput` and `*_list` (see [SearchDropdownUtils.py](../robo_appian/components/SearchDropdownUtils.py), [SearchInputUtils.py](../robo_appian/components/SearchInputUtils.py)).
- Tabs/Links/Labels: Tab selection and link clicks by visible text (see [TabUtils.py](../robo_appian/components/TabUtils.py), [LinkUtils.py](../robo_appian/components/LinkUtils.py), [LabelUtils.py](../robo_appian/components/LabelUtils.py)).

## Orchestrating Actions
- Use `ComponentDriver.execute(wait, type, action, label, value)` to route high-level steps (see [ComponentDriver.py](../robo_appian/controllers/ComponentDriver.py)).
  - Examples:
    - Dates: `("Date", "Set Value", label, value)`
    - Input: `("Input Text", "Set Value", label, value)`
    - Button: `("Button", "Click", label, None)`
    - Dropdown: `("Drop Down", "Select", label, value)`
  - When adding a new utility, wire it into the `match` blocks here with precise `type`/`action` strings.

## Reuse/Resilience Helpers
- Timeouts: Use `retry_on_timeout(operation, max_retries, operation_name)` from [RoboUtils.py](../robo_appian/utils/RoboUtils.py) to reattempt flaky waits/actions that may hit `TimeoutException`.
- Element queries: Prefer `ComponentUtils.waitForComponentToBeVisibleByXpath()` and related helpers for consistency and better diagnostics (see [ComponentUtils.py](../robo_appian/utils/ComponentUtils.py)).

## Dev Workflows
- Python version: 3.12 (see [pyproject.toml](../pyproject.toml)). Selenium >= 4.34.0 required.
- Install (dev bootstrap):
  ```bash
  pip install -r requirements.txt
  poetry install
  ```
- Lint/tests: `pytest` is declared; tests may live in consumer projects. Keep new code importable and deterministic.
- Docs (MkDocs):
  ```bash
  poetry run mkdocs serve
  ```
- Build/publish:
  ```bash
  poetry build
  # upload as needed with twine
  ```
- CI helpers: Workflow validators in [validate_simple.py](../validate_simple.py) and [validate_workflow.py](../validate_workflow.py). Useful when editing `.github/workflows/*`.

## Gotchas & Conventions
- Accessing driver: Code uses `wait._driver` consistently. If you must accept a `driver`, do it privately and keep public APIs `wait`-first.
- Exact vs partial label APIs: Most utilities expose both; choose the one that matches the page’s label stability.
- Hidden/overlay states: Favor waiting for visibility and clickability; several utilities check invisibility before proceeding.
- Table indices: Public APIs accept 0-based `rowNumber`; convert internally as needed (see [TableUtils.py](../robo_appian/components/TableUtils.py)).
- Version helper: `ComponentUtils.get_version()` reads `pyproject.toml`. It expects a standard layout; avoid moving or renaming while integrating.

If any section is unclear or you need more examples (e.g., adding a new component utility or extending `ComponentDriver`), tell me which area to expand and I’ll refine this. 