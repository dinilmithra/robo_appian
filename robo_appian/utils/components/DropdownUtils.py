from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from robo_appian.utils.components.InputUtils import InputUtils


class DropdownUtils:
    """
    Utility class for interacting with dropdown components in Appian UI.

        Usage Example:

        # Select a value from a dropdown
        from robo_appian.utils.components.DropdownUtils import DropdownUtils
        DropdownUtils.selectDropdownValue(wait, "Status", "Approved")

        # Select a value from a search dropdown
        from robo_appian.utils.components.DropdownUtils import DropdownUtils
        DropdownUtils.selectSearchDropdownValue(wait, "Category", "Finance")
    """

    @staticmethod
    def findDropdownEnabled(wait: WebDriverWait, dropdown_label: str):
        """
        Finds a dropdown component that is enabled and has the specified label.

        Parameters:
            wait: Selenium WebDriverWait instance.
            dropdown_label: The visible text label of the dropdown component.

        Returns:
            The Selenium WebElement for the dropdown component.

        Example:
            DropdownUtils.findDropdownEnabled(wait, "Status")

        """
        # This method locates a dropdown component that contains a label with the specified text.
        # It then retrieves the component's ID and uses it to find the actual dropdown element.
        # The dropdown is identified by its role as a combobox and tabindex attribute.
        # The XPath searches for a div that contains a span with the specified label text.
        # It ensures that the dropdown is clickable and ready for interaction.
        # The dropdown component is expected to have a structure where the label is within a span inside a div.

        xpath = f'.//div[./div/span[normalize-space(text())="{dropdown_label}"]]/div/div/div/div[@role="combobox" and @tabindex="0"]'
        component = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        return component

    @staticmethod
    def selectValueUsingComponent(
        wait: WebDriverWait, 
        combobox: WebElement, 
        value: str
    ) -> None:
        """
        Selects a value from a dropdown component using the provided combobox element.

        Parameters:
            wait: Selenium WebDriverWait instance.
            combobox: The Selenium WebElement for the combobox.
            value: The value to select from the dropdown.

        Example:
            DropdownUtils.selectValueUsingComponent(wait, combobox, "Approved")

        """
        # This method assumes that the combobox is already found and passed as an argument.
        # It retrieves the aria-controls attribute to find the dropdown list and selects the specified value.

        if not combobox:
            raise ValueError(f"Dropdown component object is not valid.")

        component: WebElement = combobox.find_element(By.XPATH, "./div/div")  # type: ignore[reportUnknownMemberType]
        aria_controls = component.get_attribute("aria-controls") # type: ignore[reportUnknownMemberType]
        component.click()

        xpath = f'.//div/ul[@id="{aria_controls}"]/li[./div[normalize-space(text())="{value}"]]'
        # component = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        component = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        component.click()

    @staticmethod
    def selectDropdownValue(wait: WebDriverWait, label: str, value: str) -> None:
        """
        Selects a value from a dropdown component identified by its label.

        Parameters:
            wait: Selenium WebDriverWait instance.
            label: The visible text label of the dropdown component.
            value: The value to select from the dropdown.

        Example:
            DropdownUtils.selectDropdownValue(wait, "Status", "Approved")

        """
        # This method finds the dropdown component by its label, retrieves the aria-controls attribute,
        # and then clicks on the dropdown to display the options.

        combobox = DropdownUtils.findDropdownEnabled(wait, label)
        aria_controls = combobox.get_attribute("aria-controls") # type: ignore[reportUnknownMemberType]
        combobox.click()

        xpath = f'.//div/ul[@id="{aria_controls}"]/li[./div[normalize-space(text())="{value}"]]'
        component = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        component = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        component.click()

    @staticmethod
    def selectSearchDropdownValue(wait: WebDriverWait, dropdown_label: str, value: str):
        """
        Selects a value from a search-enabled dropdown component identified by its label.

        Parameters:
            wait: Selenium WebDriverWait instance.
            dropdown_label: The visible text label of the search dropdown component.
            value: The value to select from the dropdown.

        Example:
            DropdownUtils.selectSearchDropdownValue(wait, "Category", "Finance")

        """
        # This method finds the search-enabled dropdown component by its label, retrieves the aria-controls attribute
        # and the component ID, clicks on the dropdown to display the search input,

        component = DropdownUtils.findDropdownEnabled(wait, dropdown_label)
        component_id = component.get_attribute("aria-labelledby") # type: ignore[reportUnknownMemberType]
        aria_controls = component.get_attribute("aria-controls") # type: ignore[reportUnknownMemberType]
        component.click()

        input_component_id = str(component_id) + "_searchInput"
        input_component = wait.until(
            EC.element_to_be_clickable((By.ID, input_component_id))
        )
        InputUtils.setValueUsingComponent(input_component, value)

        xpath = f'.//ul[@id="{aria_controls}"]/li[./div[normalize-space(text())="{value}"]][1]'
        component = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        component.click()
