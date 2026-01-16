from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from robo_appian.utils.ComponentUtils import ComponentUtils


class LinkUtils:
    """
    Click hyperlinks in Appian UI by their visible text.

    Find and click links using their user-visible text label. Automatically waits for
    clickability and handles hidden/overlay states. Uses ActionChains for reliable clicking
    even when links are covered by animations or tooltips.

    All methods follow the wait-first pattern: pass WebDriverWait as the first argument.

    Examples:
        >>> from robo_appian import LinkUtils
        >>> LinkUtils.click(wait, "Learn More")
        >>> LinkUtils.click(wait, "Edit Details")
        >>> link = LinkUtils.find(wait, "View Report")

    Note:
        - Uses exact text matching for link discovery
        - Excludes hidden links (aria-hidden="true") automatically
        - Returns the link element (WebElement) for advanced use cases
    """

    @staticmethod
    def find(wait: WebDriverWait, label: str):
        """
        Find a link element by its visible text.

        Locates the first link that matches the exact text, excluding hidden links.
        Useful when you need to inspect or chain operations on a link.

        Args:
            wait: WebDriverWait instance.
            label: Exact visible text of the link.

        Returns:
            WebElement: The link element (for advanced chaining).

        Raises:
            TimeoutException: If link not found within timeout.

        Examples:
            >>> link = LinkUtils.find(wait, "Edit")
            >>> link.get_attribute("href")  # Get link URL
        """
        xpath = f'.//a[normalize-space(.)="{label}" and not(ancestor::*[@aria-hidden="true"])]'
        component = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        return component

    @staticmethod
    def click(wait: WebDriverWait, label: str):
        """
        Click a link by its exact visible text.

        Finds the link by exact text match, waits for clickability, and clicks it using
        ActionChains for reliable interaction even with animations or overlays.

        Args:
            wait: WebDriverWait instance.
            label: Exact visible text of the link to click (e.g., "Edit", "Learn More").

        Returns:
            WebElement: The link element that was clicked.

        Raises:
            TimeoutException: If link not found or not clickable within timeout.

        Examples:
            >>> LinkUtils.click(wait, "Learn More")
            >>> LinkUtils.click(wait, "View Details")
            >>> LinkUtils.click(wait, "Delete")
        """

        component = LinkUtils.find(wait, label)
        ComponentUtils.click(wait, component)
        return component
