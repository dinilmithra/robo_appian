from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from robo_appian.components.InputUtils import InputUtils
from robo_appian.utils.ComponentUtils import ComponentUtils


class DateUtils:
    """
    Fill date picker components by label or interact with date input fields.

    Set dates in Appian date picker components by their associated label. Handles both
    text-based date entry and date picker interaction. Automatically waits for clickability
    and formats dates according to Appian's expected format.

    All methods follow the wait-first pattern: pass WebDriverWait as the first argument.

    Examples:
        >>> from robo_appian import DateUtils, ComponentUtils

        # Set a date value
        DateUtils.setValueByLabelText(wait, "Start Date", "01/15/2024")
        DateUtils.setValueByLabelText(wait, "End Date", "12/31/2024")

        # Use helper functions for common dates
        DateUtils.setValueByLabelText(wait, "Today", ComponentUtils.today())
        DateUtils.setValueByLabelText(wait, "Yesterday", ComponentUtils.yesterday())

        # Click to open date picker
        DateUtils.clickByLabelText(wait, "Event Date")

    Note:
        - Date format is typically MM/DD/YYYY for Appian
        - Waits for clickability before interacting with date fields
        - ComponentUtils.today() returns today's date as MM/DD/YYYY
    """

    @staticmethod
    def __findComponent(wait: WebDriverWait, label: str):
        """
        Finds a date component by its label.
        :param wait: WebDriverWait instance to wait for elements.
        :param label: The label of the date component.
        :return: The WebElement representing the date component.
        Example:
            DateUtils.__findComponent(wait, "Start Date")
        """

        xpath = f'.//div[./div/label[normalize-space(translate(., "\u00a0", " "))="{label}"]]/div/div/div/input'
        component = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        return component

    @staticmethod
    def setValueByLabelText(wait: WebDriverWait, label: str, value: str):
        """
        Set a date in a date picker component by label.

        Finds the date input by its associated label, waits for clickability, clears any
        existing date, and enters the new date value.

        Args:
            wait: WebDriverWait instance.
            label: Exact label text of the date component (e.g., "Start Date").
            value: Date string in MM/DD/YYYY format (e.g., "01/15/2024").

        Returns:
            WebElement: The date input component (for chaining if needed).

        Raises:
            ValueError: If label has no 'for' attribute.
            TimeoutException: If date input not found or not clickable within timeout.

        Examples:
            >>> DateUtils.setValueByLabelText(wait, "Start Date", "01/15/2024")
            >>> DateUtils.setValueByLabelText(wait, "End Date", "12/31/2024")
            >>> # Using helper for today's date
            >>> from robo_appian.utils.ComponentUtils import ComponentUtils
            >>> DateUtils.setValueByLabelText(wait, "Date", ComponentUtils.today())
        """
        component = DateUtils.__findComponent(wait, label)
        InputUtils._setValueByComponent(wait, component, value)
        return component

    @staticmethod
    def clickByLabelText(wait: WebDriverWait, label: str):
        """
        Clicks on the date component to open the date picker.
        :param wait: WebDriverWait instance to wait for elements.
        :param label: The label of the date component.
        :return: The WebElement representing the date component.
        Example:
            DateUtils.clickByLabelText(wait, "Start Date")
        """
        component = DateUtils.__findComponent(wait, label)

        ComponentUtils.click(wait, component)
        return component
