from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement


class InputUtils:
    """
    Utility class for interacting with input components in Appian UI.

        Usage Example:

        # Set a value in an input field
        from robo_appian.utils.components.InputUtils import InputUtils
        InputUtils.setInputValue(wait, "Username", "test_user")

    """

    @staticmethod
    def findComponent(wait: WebDriverWait, label: str):
        """
        Finds an input component by its label.

        Parameters:
            wait: Selenium WebDriverWait instance.
            label: The visible text label of the input component.

        Returns:
            The Selenium WebElement for the input component.

        Example:
            InputUtils.findComponent(wait, "Username")

        """
        # This method locates an input component that contains a label with the specified text.
        # It then retrieves the component's ID and uses it to find the actual input element.

        xpath = f".//div/label[text()='{label}']"
        component: WebElement = wait.until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )

        attribute: str = "for"
        component_id = component.get_attribute(attribute)  # type: ignore[reportUnknownMemberType]
        if not component_id:
            raise ValueError(
                f"Could not find component using {attribute} attribute for label '{label}'."
            )

        component = wait.until(EC.element_to_be_clickable((By.ID, component_id)))
        return component

    @staticmethod
    def setValueUsingComponent(component: WebElement, value: str):
        """
        Sets a value in an input component using the provided component element.

        Parameters:
            component: The Selenium WebElement for the input component.
            value: The value to set in the input field.

        Returns:
            The Selenium WebElement for the input component after setting the value.

        Example:
            InputUtils.setValueUsingComponent(component, "test_user")

        """
        # This method assumes that the component is already found and passed as an argument.
        # It clears the existing value and sets the new value in the input field.

        if not component.is_displayed():
            raise Exception(
                f"Component with label '{component.text}' is not displayed."
            )

        component.clear()
        component.send_keys(value)
        return component

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

        component = InputUtils.setValueUsingComponent(component, value)
        component.send_keys(Keys.ENTER)
        return component

    @staticmethod
    def setInputValue(wait: WebDriverWait, label: str, value: str):
        """
        Sets a value in an input component identified by its label.

        Parameters:
            wait: Selenium WebDriverWait instance.
            label: The visible text label of the input component.
            value: The value to set in the input field.

        Returns:
            The Selenium WebElement for the input component after setting the value.

        Example:
            InputUtils.setInputValue(wait, "Username", "test_user")

        """
        # This method finds the input component by its label and sets the specified value in it.
        # It retrieves the component's ID and uses it to find the actual input element.

        component = InputUtils.findComponent(wait, label)
        InputUtils.setValueUsingComponent(component, value)
        return component

    @staticmethod
    def setValueAndSubmit(wait: WebDriverWait, label: str, value: str):
        """
        Sets a value in an input component identified by its label and submits it.

        Parameters:
            wait: Selenium WebDriverWait instance.
            label: The visible text label of the input component.
            value: The value to set in the input field.

        Returns:
            The Selenium WebElement for the input component after setting the value and submitting.

        Example:
            InputUtils.setValueAndSubmit(wait, "Username", "test_user")

        """
        # This method finds the input component by its label, sets the specified value in it,
        # and submits the form by sending an ENTER key.

        component = InputUtils.findComponent(wait, label)
        component = InputUtils.setValueAndSubmitUsingComponent(component, value)
        return component

    @staticmethod
    def setSearchInputValue(wait: WebDriverWait, label: str, value: str):
        """
        Sets a value in a search-enabled input component identified by its label.

        Parameters:
            wait: Selenium WebDriverWait instance.
            label: The visible text label of the search input component.
            value: The value to set in the search input field.

        Returns:
            None
        Example:
            InputUtils.setSearchInputValue(wait, "Search", "Appian")

        """
        # This method finds the search-enabled input component by its label, retrieves the aria-controls attribute
        # and the component ID, clicks on the input to display the search input,
        # and sets the specified value in the search input field.

        xpath = (
            f".//div[./div/span[text()='{label}']]/div/div/div/input[@role='combobox']"
        )
        search_input_component = wait.until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        aria_controls = search_input_component.get_attribute("aria-controls")  # type: ignore[reportUnknownMemberType]
        InputUtils.setValueUsingComponent(search_input_component, value)

        xpath = f".//ul[@id='{aria_controls}' and @role='listbox' ]/li[@role='option']/div/div/div/div/div/div/p[text()='{value}'][1]"
        drop_down_item = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        drop_down_item.click()
