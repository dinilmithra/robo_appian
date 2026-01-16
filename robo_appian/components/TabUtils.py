from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from robo_appian.utils.ComponentUtils import ComponentUtils


class TabUtils:
    """
    Select and check tab components in Appian UI.

    Find and click tabs to navigate between sections within a single page. Appian often uses
    tabs to organize related content. Automatically waits for clickability and uses ActionChains
    for reliable interaction.

    All methods follow the wait-first pattern: pass WebDriverWait as the first argument.

    Examples:
        >>> from robo_appian import TabUtils
        >>> TabUtils.selectTabByLabelText(wait, "Details")  # Click a tab
        >>> tab = TabUtils.findTabByLabelText(wait, "History")  # Get tab element
        >>> is_selected = TabUtils.checkTabSelectedByLabelText(wait, "Active")  # Check state

    Note:
        - Tab navigation triggers content reloads; be ready to wait for new elements
        - Tab labels are stored in nested divs with role="link" and semantic text
    """

    @staticmethod
    def findTabByLabelText(wait: WebDriverWait, label: str) -> WebElement:
        """
        Find a tab element by its exact visible label.

        Returns the tab element (useful for chaining or advanced inspection).

        Args:
            wait: WebDriverWait instance.
            label: Exact visible label text of the tab (e.g., "Details", "History").

        Returns:
            WebElement: The tab element.

        Raises:
            TimeoutException: If tab not found within timeout.

        Examples:
            >>> tab = TabUtils.findTabByLabelText(wait, "Details")
        """
        xpath = f'//div/div[@role="link" ]/div/div/div/div/div/p[normalize-space(.)="{label}"]'
        component = wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
        return component

    @staticmethod
    def selectTabByLabelText(wait: WebDriverWait, label: str):
        """
        Click a tab to navigate to it by its exact visible label.

        Finds and clicks the tab. After clicking, content in the tab panel will load;
        be ready to wait for elements within the new tab.

        Args:
            wait: WebDriverWait instance.
            label: Exact visible label text of the tab to select.

        Returns:
            None

        Raises:
            TimeoutException: If tab not found or not clickable within timeout.

        Examples:
            >>> TabUtils.selectTabByLabelText(wait, "Details")
            >>> TabUtils.selectTabByLabelText(wait, "History")
        """
        component = TabUtils.findTabByLabelText(wait, label)
        ComponentUtils.click(wait, component)

    @staticmethod
    def checkTabSelectedByLabelText(wait: WebDriverWait, label: str):
        """
        Check if a tab is currently selected (active).

        Returns True if the tab has the "Selected Tab" indicator (aria-label or span text),
        False otherwise. Useful in test assertions to verify navigation.

        Args:
            wait: WebDriverWait instance.
            label: Exact visible label text of the tab to check.

        Returns:
            bool: True if tab is selected, False otherwise (or if tab not found).

        Examples:
            >>> if TabUtils.checkTabSelectedByLabelText(wait, "Details"):
            ...     print("Details tab is active")
            >>> assert TabUtils.checkTabSelectedByLabelText(wait, "History"), "History tab should be selected"
        """
        component = TabUtils.findTabByLabelText(wait, label)

        select_text = "Selected Tab."
        xpath = f'./span[normalize-space(.)="{select_text}"]'
        try:
            component = ComponentUtils.findChildComponentByXpath(wait, component, xpath)
        except Exception:
            return False

        return True
