from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from robo_appian.components.InputUtils import InputUtils


class DateUtils:
    """
    Utility class for interacting with date components in Appian UI.

        Usage Example:

        # Set a date value
        from robo_appian.components.DateUtils import DateUtils
        DateUtils.setDateValue(wait, "Start Date", "01/01/2024")

    """

    @staticmethod
    def findComponent(wait: WebDriverWait, label: str):
        """
        Finds a date component by its label.

        Parameters:
            wait: Selenium WebDriverWait instance.
            label: The visible text label of the date component.

        Returns:
            The Selenium WebElement for the date component.

        Example:
            DateUtils.findComponent(wait, "Start Date")

        """

        xpath = f".//div/label[text()='{label}']"
        component: WebElement = wait.until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        if not component:
            raise ValueError(f"Could not find date component with label '{label}'.")

        attribute: str = "for"
        component_id = component.get_attribute(attribute)  # type: ignore[reportUnknownMemberType]
        if component_id is None:
            raise ValueError(
                f"Could not find component using {attribute} attribute for label '{label}'."
            )

        component = wait.until(EC.element_to_be_clickable((By.ID, component_id)))
        return component

    @staticmethod
    def setDateValue(wait: WebDriverWait, label: str, value: str):
        """
        Sets a date value in a date component identified by its label.

        Parameters:
            wait: Selenium WebDriverWait instance.
            label: The visible text label of the date component.
            value: The date value to set (e.g., "01/01/2024").

        Returns:
            The Selenium WebElement for the date component after setting the value.

        Example:
            DateUtils.setDateValue(wait, "Start Date", "01/01/2024")

        """
        # This method locates a date component that contains a label with the specified text.
        # It then retrieves the component's ID and uses it to find the actual input element.
        # component = wait.until(EC.element_to_be_clickable((By.XPATH, f".//div/label[text()='{label}']/following-sibling::input")))

        component = DateUtils.findComponent(wait, label)
        InputUtils._setComponentValue(component, value)
        return component

    @staticmethod
    def setDateValueAndSubmit(wait: WebDriverWait, label: str, value: str):
        """
        Sets a date value in a date component identified by its label and submits the form.

        Parameters:
            wait: Selenium WebDriverWait instance.
            label: The visible text label of the date component.
            value: The date value to set (e.g., "01/01/2024").

        Returns:
            The Selenium WebElement for the date component after setting the value.

        Example:
            DateUtils.setDateValueAndSubmit(wait, "Start Date", "01/01/2024")

        """

        # This method locates a date component that contains a label with the specified text.
        # It then retrieves the component's ID and uses it to find the actual input element.
        # It sets the value of the input element and submits it.

        component = DateUtils.findComponent(wait, label)
        InputUtils.setValueAndSubmitUsingComponent(component, value)

        return component

    @staticmethod
    def click(wait: WebDriverWait, label: str):
        """
        Clicks on a date component identified by its label.

        Parameters:
            wait: Selenium WebDriverWait instance.
            label: The visible text label of the date component.

        Returns:
            The Selenium WebElement for the date component after clicking.

        Example:
            DateUtils.click(wait, "Start Date")
        """
        # This method locates a date component that contains a label with the specified text.
        # It then retrieves the component's ID and uses it to find the actual input element.
        # It clicks on the input element to open the date picker.

        component = DateUtils.findComponent(wait, label)
        component.click()

        return component
