from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from robo_appian.components.InputUtils import InputUtils
from robo_appian.utils.ComponentUtils import ComponentUtils


class DateUtils:
    """
    Utility class for interacting with date components in Appian UI.
    Usage Example:
        # Set a date value in a date component
        from robo_appian.components.DateUtils import DateUtils
        DateUtils.setValueByLabelText(wait, "Start Date", "2023-10-01")
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
        try:
            component = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        except Exception as e:
            raise Exception(
                f"Could not find clickable date component with label '{label}': {e}"
            )
        return component

    @staticmethod
    def setValueByLabelText(wait: WebDriverWait, label: str, value: str):
        """
        Sets the value of a date component.
        :param wait: WebDriverWait instance to wait for elements.
        :param label: The label of the date component.
        :param value: The value to set in the date component.
        :return: The WebElement representing the date component.
        Example:
            DateUtils.setValueByLabelText(wait, "Start Date", "2023-10-01")
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
