from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from robo_appian.utils.ComponentUtils import ComponentUtils


class LabelUtils:
    """
    Find and click text labels and headings in Appian UI.

    Use these utilities to check for the presence of labels, headers, or other text elements
    that don't fit into form component categories. Useful for validation steps that verify
    page content or labels before/after actions.

    All methods follow the wait-first pattern: pass WebDriverWait as the first argument.

    Examples:
        >>> from robo_appian import LabelUtils
        >>> LabelUtils.clickByLabelText(wait, "Expand")
        >>> if LabelUtils.isLabelExists(wait, "Success!"):
        ...     print("Operation completed")

    Note:
        - Handles NBSP characters automatically via normalize-space
        - Supports existence checks for validation and assertions
        - Useful in test assertions: `assert LabelUtils.isLabelExists(wait, "Pending")`
    """

    @staticmethod
    def __findByLabelText(wait: WebDriverWait, label: str):
        """
        Find a label element by exact text (internal helper).

        Args:
            wait: WebDriverWait instance.
            label: Exact visible text of the label.

        Returns:
            WebElement: The label element.

        Raises:
            TimeoutException: If label not found within timeout.
        """
        xpath = f'//*[normalize-space(translate(., "\u00a0", " "))="{label}"]'
        component = ComponentUtils.waitForComponentToBeVisibleByXpath(wait, xpath)
        return component

    @staticmethod
    def clickByLabelText(wait: WebDriverWait, label: str):
        """
        Click a label or text element by its exact visible text.

        Find and click text elements that trigger UI changes (e.g., collapsible headers).

        Args:
            wait: WebDriverWait instance.
            label: Exact visible text of the element to click.

        Returns:
            None

        Raises:
            TimeoutException: If element not found or not clickable within timeout.

        Examples:
            >>> LabelUtils.clickByLabelText(wait, "Expand")
            >>> LabelUtils.clickByLabelText(wait, "Show Details")
        """
        component = LabelUtils.__findByLabelText(wait, label)
        ComponentUtils.click(wait, component)

    @staticmethod
    def isLabelExists(wait: WebDriverWait, label: str):
        """
        Check if a label with the exact text exists on the page.

        Non-blocking check useful in test assertions and conditional logic.
        Returns False if label not found or times out (doesn't raise exception).

        Args:
            wait: WebDriverWait instance.
            label: Exact visible text to search for.

        Returns:
            bool: True if label found and visible, False otherwise.

        Examples:
            >>> if LabelUtils.isLabelExists(wait, "Error: Invalid input"):
            ...     print("Validation error displayed")
            >>> assert LabelUtils.isLabelExists(wait, "Success!"), "Success message not found"
        """
        try:
            LabelUtils.__findByLabelText(wait, label)
        except Exception:
            return False
        return True

    @staticmethod
    def isLabelExistsAfterLoad(wait: WebDriverWait, label: str):
        """
        Check if a label exists after waiting for visibility (stricter validation).

        Waits explicitly for the element to become visible, unlike isLabelExists which
        may find invisible elements. Use this when page is still loading.

        Args:
            wait: WebDriverWait instance.
            label: Exact visible text to search for.

        Returns:
            bool: True if label becomes visible within timeout, False otherwise.

        Examples:
            >>> # Wait for success message to appear after form submission
            >>> if LabelUtils.isLabelExistsAfterLoad(wait, "Saved successfully"):
            ...     print("Form saved")
        """
        try:
            xpath = f'.//*[normalize-space(translate(., "\u00a0", " "))="{label}"]'
            wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
        except Exception:
            return False
        return True
