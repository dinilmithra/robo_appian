# API Reference

All robo_appian APIs are page-first. Pass a Playwright `page` as the first argument.

Use the individual utility classes for direct interactions, or route data-driven steps through `ComponentDriver.execute(page, type, action, label, value)`.

## Utilities
- BrowserUtils: Browser tab helpers.
- ButtonUtils: Click buttons by exact or partial label.
- ComponentDriver: Route high-level actions to the correct utility.
- ComponentUtils: Shared waits, clicks, XPath helpers, and date/version helpers.
- DateUtils: Fill date inputs by label.
- DropdownUtils: Select values from Appian dropdowns.
- InputUtils: Fill text inputs by label, id, or placeholder.
- LabelUtils: Check and click visible text labels.
- LinkUtils: Click links by exact text.
- RoboUtils: Retry flaky timeout-prone actions.
- SearchDropdownUtils: Type-and-select search dropdown values.
- SearchInputUtils: Type-and-select search input values.
- TabUtils: Find, click, and verify tabs.
- TableUtils: Locate rows and cells by column name.
