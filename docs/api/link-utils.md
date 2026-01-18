# Link Utils

## Overview

LinkUtils provides methods to find and click hyperlinks in Appian UI. Use LinkUtils to interact with links using their visible text label. Automatically waits for clickability and handles hidden or overlay states.

## Methods

### click

Click a hyperlink by its exact visible text.

Use this when you need to navigate by clicking a link and you know the exact text displayed on the link. This method waits for the link to be clickable and uses ActionChains for reliable interaction even when links are covered by animations, tooltips, or other overlays.

**Args:**

- `wait` (WebDriverWait): WebDriverWait instance with configured timeout
- `label` (str): Exact visible text of the link to click

**Raises:**

- `TimeoutException`: If link not found or not clickable within timeout

**Returns:** WebElement representing the link that was clicked

**Examples:**

HTML:
```html
<div class="navigation">
  <a href="/details">View Details</a>
  <a href="/edit">Edit</a>
  <a href="/help">Learn More</a>
</div>
```

Python:
```python
from robo_appian.components.LinkUtils import LinkUtils
from selenium.webdriver.support.ui import WebDriverWait

LinkUtils.click(wait, "Learn More")
```

---

### find

Find a link element by its exact visible text without clicking it.

Use this when you need to inspect a link element or perform custom operations on it before clicking. Returns the link WebElement for advanced use cases like checking the href attribute, getting link text, or validating link properties. Most commonly you'll use the click method instead, but this is useful for validation or custom interactions.

**Args:**

- `wait` (WebDriverWait): WebDriverWait instance with configured timeout
- `label` (str): Exact visible text of the link

**Raises:**

- `TimeoutException`: If link not found within timeout

**Returns:** WebElement representing the link element

**Examples:**

HTML:
```html
<div class="navigation">
  <a href="/profile/edit">Edit Profile</a>
  <a href="/settings">Settings</a>
</div>
```

Python:
```python
from robo_appian.components.LinkUtils import LinkUtils
from selenium.webdriver.support.ui import WebDriverWait

link = LinkUtils.find(wait, "Edit Profile")
print(f"Link URL: {link.get_attribute('href')}")
assert "/profile/edit" in link.get_attribute('href'), "Incorrect link URL"
```