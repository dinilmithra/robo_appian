from numpy import size
from robo_appian.utils.ComponentUtils import ComponentUtils
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from typing import List


class InputUtils:
    """
    Utility class for interacting with input components in Appian UI.

        Usage Example:

        # Set a value in an input field
        from robo_appian.components.InputUtils import InputUtils
        InputUtils.setValueByLabelText(wait, "Username", "test_user")

    """

    @staticmethod
    def setValueAndSubmitUsingComponent(component: WebElement, value: str):
        """
        Sets a value in an input component and submits it using the provided component element.

        Parameters:
            component: The Selenium WebElement for the input component.
            value: The value to set in the input field.

        Returns:
            The Selenium WebElement for the input component after setting the value and submitting.

        Example:
            InputUtils.setValueAndSubmitUsingComponent(component, "test_user")

        """
        # This method assumes that the component is already found and passed as an argument.

        if not component.is_displayed():
            raise Exception(
                f"Component with label '{component.text}' is not displayed."
            )

        component = InputUtils._setComponentValue(component, value)
        component.send_keys(Keys.ENTER)
        return component

    @staticmethod
    def __findInputComponentsByLabelPath(wait: WebDriverWait, xpath: str):
        label_components = ComponentUtils.findComponentsByXPath(wait, xpath)
        input_components = []
        for label_component in label_components:
            attribute: str = "for"
            component_id = label_component.get_attribute(attribute)  # type: ignore[reportUnknownMemberType]
            if component_id:
                component = wait.until(
                    EC.element_to_be_clickable((By.ID, component_id))
                )
                input_components.append(component)
        return input_components

    @staticmethod
    def __findInputComponentsByPartialLabel(wait: WebDriverWait, label: str):
        xpath = f'.//div/label[contains(normalize-space(text()), "{label}")]'
        components = InputUtils.__findInputComponentsByLabelPath(wait, xpath)
        return components

    @staticmethod
    def __findInputComponentsByLabel(wait: WebDriverWait, label: str):
        xpath = f'.//div/label[normalize-space(text())="{label}"]'
        components = InputUtils.__findInputComponentsByLabelPath(wait, xpath)
        return components

    @staticmethod
    def _setComponentValue(component: WebElement, value: str):
        component.clear()
        component.send_keys(value)
        return component

    @staticmethod
    def __setValueByComponents(wait: WebDriverWait, input_components, value: str):
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

        for component in input_components:
            InputUtils._setComponentValue(component, value)

    @staticmethod
    def setValueByPartialLabelText(wait: WebDriverWait, label: str, value: str):
        input_components = InputUtils.__findInputComponentsByPartialLabel(wait, label)
        InputUtils.__setValueByComponents(wait, input_components, value)

    @staticmethod
    def setValueByLabelText(wait: WebDriverWait, label: str, value: str):
        input_components = InputUtils.__findInputComponentsByLabel(wait, label)
        InputUtils.__setValueByComponents(wait, input_components, value)
