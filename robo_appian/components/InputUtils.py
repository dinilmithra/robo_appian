from robo_appian.utils.ComponentUtils import ComponentUtils
from selenium.webdriver.common.by import By
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
    def __findInputComponentsByXpath(wait: WebDriverWait, xpath: str):
        """
        Finds input components by their XPath.

        Parameters:
            wait: Selenium WebDriverWait instance.
            xpath: The XPath expression to locate the input components.

        Returns:
            A list of Selenium WebElement representing the input components.

        Example:
            InputUtils.__findInputComponentsByXpath(wait, './/div/label[normalize-space(text())="Username"]')
        """
        label_components = ComponentUtils.findComponentsByXPath(wait, xpath)
        input_components = []
        for label_component in label_components:
            attribute: str = "for"
            component_id = label_component.get_attribute(attribute)  # type: ignore[reportUnknownMemberType]
            if component_id:
                try:
                    component = wait.until(EC.element_to_be_clickable((By.ID, component_id)))
                    input_components.append(component)
                except Exception as e:
                    raise Exception(f"Could not find clickable input component with id '{component_id}': {e}")
            else:
                raise ValueError(f"Input component with label '{label_component.text}' does not have 'for' attribute.")
        return input_components

    @staticmethod
    def __findInputComponentsByPartialLabel(wait: WebDriverWait, label: str):
        """Finds input components by their label text, allowing for partial matches.

        Parameters:
            wait: Selenium WebDriverWait instance.
            label: The visible text label of the input component, allowing for partial matches.

        Returns:
            A list of Selenium WebElement representing the input components.

        Example:
            InputUtils.__findInputComponentsByPartialLabel(wait, "Username")
        """
        xpath = f'.//div/label[contains(normalize-space(text()), "{label}")]'
        components = InputUtils.__findInputComponentsByXpath(wait, xpath)
        return components

    @staticmethod
    def __findComponentsByLabel(wait: WebDriverWait, label: str):
        """Finds input components by their label text.

        Parameters:
            wait: Selenium WebDriverWait instance.
            label: The visible text label of the input component.

        Returns:
            A list of Selenium WebElement representing the input components.

        Example:
            InputUtils.__findComponentsByLabel(wait, "Username")
        """
        xpath = f'.//div/label[normalize-space(text())="{label}"]'
        components = InputUtils.__findInputComponentsByXpath(wait, xpath)
        return components

    @staticmethod
    def _setValueByComponent(component: WebElement, value: str):
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
            InputUtils._setValueByComponent(component, value)

    @staticmethod
    def setValueByPartialLabelText(wait: WebDriverWait, label: str, value: str):
        input_components = InputUtils.__findInputComponentsByPartialLabel(wait, label)
        InputUtils.__setValueByComponents(wait, input_components, value)

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
        input_components = InputUtils.__findComponentsByLabel(wait, label)
        InputUtils.__setValueByComponents(wait, input_components, value)

    @staticmethod
    def setValueById(wait: WebDriverWait, component_id: str, value: str):
        """
        Sets a value in an input component identified by its ID.

        Parameters:
            wait: Selenium WebDriverWait instance.
            component_id: The ID of the input component.
            value: The value to set in the input field.

        Returns:
            The Selenium WebElement for the input component after setting the value.

        Example:
            InputUtils.setValueById(wait, "inputComponentId", "test_value")
        """
        try:
            component = wait.until(EC.element_to_be_clickable((By.ID, component_id)))
        except Exception as e:
            raise Exception(f"Timeout or error finding input component with id '{component_id}': {e}")
        InputUtils._setValueByComponent(component, value)
        return component
