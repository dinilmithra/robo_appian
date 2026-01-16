from robo_appian.utils.ComponentUtils import ComponentUtils
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains


class InputUtils:
    """
    Fill text inputs, search fields, and other input components using label-driven selectors.

    This utility handles text inputs by their visible labels, making tests readable and maintainable.
    Automatically waits for clickability, clears existing values, and enters new text.

    All methods follow the wait-first pattern: pass WebDriverWait as the first argument.

    Examples:
        >>> from robo_appian import InputUtils

        # Set value by exact label match
        InputUtils.setValueByLabelText(wait, "Username", "john_doe")
        InputUtils.setValueByLabelText(wait, "Email Address", "john@example.com")

        # Set value by partial label match (useful for dynamic labels)
        InputUtils.setValueByPartialLabelText(wait, "First", "John")

        # Set value by element ID
        InputUtils.setValueById(wait, "email_input_123", "john@example.com")

        # Set value by placeholder text
        InputUtils.setValueByPlaceholderText(wait, "Enter your name", "John Doe")

    Note:
        - Uses normalize-space and NBSP translation to handle whitespace variations
        - Automatically moves to element, clears it, and enters text via ActionChains
        - Waits for element to be clickable before interacting
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
            wait: Selenium WebDriverWait instance.
            component: The Selenium WebElement for the input component.
            value: The value to set in the input field.
        Returns:
            The Selenium WebElement for the input component after setting the value.
        Example:
            InputUtils._setValueByComponent(wait, component, "test_value")
        """
        wait.until(EC.element_to_be_clickable(component))
        driver = wait._driver
        ActionChains(driver).move_to_element(component).perform()
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
        Set value in an input field by its exact label text.

        Finds the input by its associated label, waits for clickability, clears any existing
        text, and enters the new value. Most commonly used method for form filling.

        Args:
            wait: WebDriverWait instance (required by all robo_appian utilities).
            label: Exact visible label text. Must match exactly (e.g., "First Name", not "First").
            value: Text to enter into the input field.

        Raises:
            ValueError: If label element has no 'for' attribute linking to input.
            TimeoutException: If label or input not found within wait timeout.

        Examples:
            >>> InputUtils.setValueByLabelText(wait, "Username", "john_doe")
            >>> InputUtils.setValueByLabelText(wait, "Email", "john@example.com")
            >>> InputUtils.setValueByLabelText(wait, "Address", "123 Main St")
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
