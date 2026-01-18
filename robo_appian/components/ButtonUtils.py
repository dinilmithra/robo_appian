from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from robo_appian.utils.ComponentUtils import ComponentUtils


class ButtonUtils:
    """
    Click buttons, action links, and control components using visible text labels.

    Find and interact with buttons by their user-visible text. All methods automatically
    handle whitespace variations and work reliably with overlaid or animated elements.

    All methods follow the wait-first pattern: pass WebDriverWait as the first argument.

    Examples:
        >>> from robo_appian import ButtonUtils

        # Click by exact label match
        ButtonUtils.clickByLabelText(wait, "Submit")
        ButtonUtils.clickByLabelText(wait, "Save Changes")

        # Click by partial label match (useful for buttons with dynamic text)
        ButtonUtils.clickByPartialLabelText(wait, "Save")

        # Click by element ID (when labels are unavailable)
        ButtonUtils.clickById(wait, "save_button_123")

        # Check if button exists before clicking
        if ButtonUtils.isButtonExistsByLabelText(wait, "Delete"):
            ButtonUtils.clickByLabelText(wait, "Delete")
    """

    @staticmethod
    def _findByPartialLabelText(wait: WebDriverWait, label: str):
        """
        Finds a button by its label.

        Parameters:
            wait: Selenium WebDriverWait instance.
            label: The label of the button to find.

        Returns:
            WebElement representing the button.

        Example:
            component = ButtonUtils._findByPartialLabelText(wait, "Submit")
        """
        xpath = f"//button[./span[contains(translate(normalize-space(.), '\u00a0', ' '), '{label}')]]"
        return ComponentUtils.waitForComponentToBeVisibleByXpath(wait, xpath)

    @staticmethod
    def __findByLabelText(wait: WebDriverWait, label: str):
        xpath = f".//button[./span[normalize-space(.)='{label}']]"
        return ComponentUtils.waitForComponentToBeVisibleByXpath(wait, xpath)

    @staticmethod
    def clickByPartialLabelText(wait: WebDriverWait, label: str):
        """
        Finds a button by its partial label and clicks it.

        Parameters:
            wait: Selenium WebDriverWait instance.
            label: The partial label of the button to click.
            Example:
                ButtonUtils.clickByPartialLabelText(wait, "Button Label")
        """
        component = ButtonUtils._findByPartialLabelText(wait, label)

        ComponentUtils.click(wait, component)

    @staticmethod
    def clickByLabelText(wait: WebDriverWait, label: str):
        """
        Click a button by its exact label text.

        Finds and clicks a button element containing the exact label text, handling whitespace
        and NBSP characters reliably through normalized matching.

        Args:
            wait: WebDriverWait instance.
            label: Exact button text (e.g., "Submit", "Save", "Cancel").

        Raises:
            TimeoutException: If button not found or not clickable within timeout.

        Examples:
            >>> ButtonUtils.clickByLabelText(wait, "Submit")
            >>> ButtonUtils.clickByLabelText(wait, "Save Changes")
            >>> ButtonUtils.clickByLabelText(wait, "Cancel")
        """
        component = ButtonUtils.__findByLabelText(wait, label)

        ComponentUtils.click(wait, component)

    @staticmethod
    def clickById(wait: WebDriverWait, id: str):
        """Click a button by its HTML id attribute.

        Finds and clicks a button using its HTML id. Use when label-based locators
        are unavailable or unreliable.

        Args:
            wait: WebDriverWait instance.
            id: The HTML id of the button element.

        Raises:
            TimeoutException: If button not found or not clickable within timeout.

        Examples:
            >>> ButtonUtils.clickById(wait, "save_button")
            >>> ButtonUtils.clickById(wait, "submit_btn_123")
        """
        component = wait.until(EC.element_to_be_clickable((By.ID, id)))
        ComponentUtils.click(wait, component)

    @staticmethod
    def isButtonExistsByLabelText(wait: WebDriverWait, label: str):
        """
        Check if a button exists by exact label match.

        Searches for a button with the exact label text and returns True if found.
        Does not raise exceptions; returns boolean result.

        Args:
            wait: WebDriverWait instance.
            label: Exact button label text to match.

        Returns:
            bool: True if button found, False otherwise.

        Examples:
            >>> if ButtonUtils.isButtonExistsByLabelText(wait, "Delete"):
            ...     ButtonUtils.clickByLabelText(wait, "Delete")
        """
        xpath = f".//button[./span[normalize-space(.)='{label}']]"
        try:
            ComponentUtils.findComponentByXPath(wait, xpath)
        except Exception:
            return False
        return True

    @staticmethod
    def isButtonExistsByPartialLabelText(wait: WebDriverWait, label: str):
        """
        Check if a button exists by partial label match.

        Searches for a button containing the partial label text. Returns True if found, False otherwise.
        Does not raise exceptions.

        Args:
            wait: WebDriverWait instance.
            label: Partial button label text to match.

        Returns:
            bool: True if button found, False otherwise.
        """
        xpath = f".//button[./span[contains(translate(normalize-space(.), '\u00a0', ' '), '{label}')]]"
        try:
            ComponentUtils.findComponentByXPath(wait, xpath)
        except Exception:
            return False
        return True

    @staticmethod
    def isButtonExistsByPartialLabelTextAfterLoad(wait: WebDriverWait, label: str):
        """
        Check if a button exists by partial label match after page load.

        Validates button presence after page reloads or dynamic content loading.
        Returns True if found, False otherwise.

        Args:
            wait: WebDriverWait instance.
            label: Partial button label text to match.

        Returns:
            bool: True if button found and visible, False otherwise.
        """
        xpath = f".//button[./span[contains(translate(normalize-space(.), '\u00a0', ' '), '{label}')]]"
        try:
            ComponentUtils.waitForComponentToBeVisibleByXpath(wait, xpath)
            return True
        except Exception:
            return False

    @staticmethod
    def waitForButtonToBeVisibleByPartialLabelText(wait: WebDriverWait, label: str):
        """
        Wait for a button to be visible by partial label match.

        Blocks until a button containing the partial label text becomes visible
        or timeout occurs.

        Args:
            wait: WebDriverWait instance.
            label: Partial button label text to match.

        Returns:
            WebElement: The visible button element.

        Raises:
            TimeoutException: If button not visible within timeout.

        Examples:
            >>> ButtonUtils.waitForButtonToBeVisibleByPartialLabelText(wait, "Submit")
            >>> ButtonUtils.clickByPartialLabelText(wait, "Submit")
        """
        xpath = f".//button[./span[contains(translate(normalize-space(.), '\u00a0', ' '), '{label}')]]"
        return ComponentUtils.waitForComponentToBeVisibleByXpath(wait, xpath)
