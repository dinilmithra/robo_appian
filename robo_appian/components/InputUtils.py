
from robo_appian.utils.ComponentUtils import ComponentUtils
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement


class InputUtils:
    """
    Utility class for interacting with input components in Appian UI.
    Usage Example:
        from robo_appian.components.InputUtils import InputUtils

        # Set a value in an input component by its label
        InputUtils.setValueByLabelText(wait, "Username", "test_user")

        # Set a value in an input component by its ID
        InputUtils.setValueById(wait, "inputComponentId", "test_value")
    """

    @staticmethod
    def __findComponentByPartialLabel(wait: WebDriverWait, label: str):
        """
        Finds an input component by its label text, allowing for partial matches.

        Parameters:
            wait: Selenium WebDriverWait instance.
            label: The visible text label of the input component, allowing for partial matches.

        Returns:
            A Selenium WebElement representing the input component.

        Example:
            InputUtils.__findInputComponentByPartialLabel(wait, "User")
        """

        xpath = f'.//div/label[contains(normalize-space(.), "{label}")]'
        label_component = ComponentUtils.waitForComponentToBeVisibleByXpath(wait, xpath)

        input_id = label_component.get_attribute("for")
        if input_id is None:
            raise ValueError(
                f"Label component with text '{label}' does not have a 'for' attribute."
            )

        component = ComponentUtils.findComponentById(wait, input_id)
        return component

    @staticmethod
    def __findComponentByLabel(wait: WebDriverWait, label: str):
        """Finds a component by its label text.
        Parameters:
            wait: Selenium WebDriverWait instance.
            label: The visible text label of the input component.

        Returns:
            A Selenium WebElement representing the input component.

        Example:
            InputUtils.__findComponentByLabel(wait, "Username")
        """

        xpath = f'.//div/label[normalize-space(.)="{label}"]'
        label_component = ComponentUtils.waitForComponentToBeVisibleByXpath(wait, xpath)
        input_id = label_component.get_attribute("for")
        if input_id is None:
            raise ValueError(
                f"Label component with text '{label}' does not have a 'for' attribute."
            )

        component = ComponentUtils.findComponentById(wait, input_id)
        return component

    @staticmethod
    def _setValueByComponent(wait: WebDriverWait, component: WebElement, value: str):
        """
        Sets a value in an input component.
        Parameters:
            component: The Selenium WebElement for the input component.
            value: The value to set in the input field.
        Returns:
            The Selenium WebElement for the input component after setting the value.
        Example:
            InputUtils._setValueByComponent(component, "test_value")
        """
        wait.until(EC.element_to_be_clickable(component))
        component.clear()
        component.send_keys(value)
        return component

    @staticmethod
    def setValueByPartialLabelText(wait: WebDriverWait, label: str, value: str):
        """
        Sets a value in an input component identified by its partial label text.

        Parameters:
            wait: Selenium WebDriverWait instance.
            label: The visible text label of the input component (partial match).
            value: The value to set in the input field.

        Returns:
            None
        """
        component = InputUtils.__findComponentByPartialLabel(wait, label)
        InputUtils._setValueByComponent(wait, component, value)

    @staticmethod
    def setValueByLabelText(wait: WebDriverWait, label: str, value: str):
        """
        Sets a value in an input component identified by its label text.

        Parameters:
            wait: Selenium WebDriverWait instance.
            label: The visible text label of the input component.
            value: The value to set in the input field.

        Returns:
            None

        Example:
            InputUtils.setValueByLabelText(wait, "Username", "test_user")
        """
        component = InputUtils.__findComponentByLabel(wait, label)
        InputUtils._setValueByComponent(wait, component, value)

    @staticmethod
    def setValueById(wait: WebDriverWait, id: str, value: str):
        """
        Sets a value in an input component identified by its ID.

        Parameters:
            wait: Selenium WebDriverWait instance.
            id: The ID of the input component.
            value: The value to set in the input field.

        Returns:
            The Selenium WebElement for the input component after setting the value.

        Example:
            InputUtils.setValueById(wait, "inputComponentId", "test_value")
        """
        # try:
        #     component = wait.until(EC.element_to_be_clickable((By.ID, component_id)))
        # except Exception as e:
        #     raise Exception(f"Timeout or error finding input component with id '{component_id}': {e}")
        component = ComponentUtils.findComponentById(wait, id)
        InputUtils._setValueByComponent(wait, component, value)

    @staticmethod
    def setValueByPlaceholderText(wait: WebDriverWait, text: str, value: str):
        """Sets a value in an input component identified by its placeholder text.

        Parameters:
            wait: Selenium WebDriverWait instance.
            text: The placeholder text of the input component.
            value: The value to set in the input field.

        Returns:
            None

        Example:
            InputUtils.setValueByPlaceholderText(wait, "Enter your name", "John Doe")
        """
        xpath = f'.//input[@placeholder="{text}"]'
        component = ComponentUtils.waitForComponentToBeVisibleByXpath(wait, xpath)
        InputUtils._setValueByComponent(wait, component, value)
