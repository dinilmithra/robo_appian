# Browser Utils

`BrowserUtils` manages Playwright tabs for page-first tests.

## Methods
- `switch_to_Tab(page, tab_number)`: Bring a tab to the foreground by zero-based index.
- `switch_to_next_tab(page)`: Cycle to the next open tab.
- `close_current_tab_and_switch_back(page)`: Close the current tab and return to the previous open tab.

## Example
```python
current = BrowserUtils.switch_to_Tab(page, 1)
next_page = BrowserUtils.switch_to_next_tab(current)
BrowserUtils.close_current_tab_and_switch_back(next_page)
```
