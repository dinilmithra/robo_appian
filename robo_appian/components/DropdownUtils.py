import stat
from turtle import st
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from robo_appian.components.InputUtils import InputUtils


class DropdownUtils:
    """
    Utility class for interacting with dropdown components in Appian UI.

        Usage Example:

        # Select a value from a dropdown
        from robo_appian.components.DropdownUtils import DropdownUtils
        DropdownUtils.selectDropdownValueByLabelText(wait, "Status", "Approved")

        # Select a value from a search dropdown
        from robo_appian.components.DropdownUtils import DropdownUtils
        DropdownUtils.selectSearchDropdownValueByLabelText(wait, "Category", "Finance")
    """

    @staticmethod
    def __findDropdownComponentsByXpath(wait: WebDriverWait, xpath: str):

        try:
            # Wait for at least one element to be present
            wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))

            # Find all matching elements
            driver = wait._driver
            components = driver.find_elements(By.XPATH, xpath)

            # Filter for clickable and displayed components
            valid_components = []
            for component in components:
                try:
                    if component.is_displayed() and component.is_enabled():
                        valid_components.append(component)
                except Exception:
                    continue

            if not valid_components:
                raise Exception(
                    f'No valid dropdown components with xpath "{xpath}" found.'
                )

            # Return single component if only one found, list if multiple
            return valid_components

        except Exception as e:
            raise Exception(
                f'Dropdown component with xpath "{xpath}" not found: {str(e)}'
            )

    @staticmethod
    def selectDropdownValueByComponent(wait, combobox, value):
        dropdown_id = combobox.get_attribute("aria-controls")  # type: ignore[reportUnknownMemberType]
        combobox.click()

        option_xpath = f'.//div/ul[@id="{dropdown_id}"]/li[./div[normalize-space(text())="{value}"]]'
        component = wait.until(EC.presence_of_element_located((By.XPATH, option_xpath)))
        component = wait.until(EC.element_to_be_clickable((By.XPATH, option_xpath)))
        component.click()

    @staticmethod
    def __selectDropdownValueByXpath(wait, xpath, value):
        components = DropdownUtils.__findDropdownComponentsByXpath(wait, xpath)
        for combobox in components:
            if combobox.is_displayed() and combobox.is_enabled():
                DropdownUtils.selectDropdownValueByComponent(wait, combobox, value)

    @staticmethod
    def selectDropdownValueByLabelText(
        wait: WebDriverWait, dropdown_label: str, value: str
    ):

        xpath = f'.//div[./div/span[normalize-space(text())="{dropdown_label}"]]/div/div/div/div[@role="combobox" and @tabindex="0"]'
        DropdownUtils.__selectDropdownValueByXpath(wait, xpath, value)

    @staticmethod
    def selectDropdownValueByPartialLabelText(
        wait: WebDriverWait, dropdown_label: str, value: str
    ):

        xpath = f'.//div[./div/span[contains(normalize-space(text()), "{dropdown_label}")]]/div/div/div/div[@role="combobox" and @tabindex="0"]'
        DropdownUtils.__selectDropdownValueByXpath(wait, xpath, value)

    @staticmethod
    def __selectSearchDropdownValueByXpath(wait, xpath, value):

        components = DropdownUtils.__findDropdownComponentsByXpath(wait, xpath)

        for component in components:
            if component.is_displayed() and component.is_enabled():
                component_id = component.get_attribute("aria-labelledby")  # type: ignore[reportUnknownMemberType]
                dropdown_id = component.get_attribute("aria-controls")  # type: ignore[reportUnknownMemberType]
                component.click()

                input_component_id = str(component_id) + "_searchInput"
                input_component = wait.until(
                    EC.element_to_be_clickable((By.ID, input_component_id))
                )
                InputUtils._setComponentValue(input_component, value)

                xpath = f'.//ul[@id="{dropdown_id}"]/li[./div[normalize-space(text())="{value}"]][1]'
                component = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
                component.click()

    @staticmethod
    def selectSearchDropdownValueByLabelText(
        wait: WebDriverWait, dropdown_label: str, value: str
    ):
        xpath = f'.//div[./div/span[normalize-space(text())="{dropdown_label}"]]/div/div/div/div[@role="combobox" and @tabindex="0"]'
        DropdownUtils.__selectSearchDropdownValueByXpath(wait, xpath, value)

    @staticmethod
    def selectSearchDropdownValueByPartialLabelText(
        wait: WebDriverWait, dropdown_label: str, value: str
    ):

        xpath = f'.//div[./div/span[contains(normalize-space(text()), "{dropdown_label}")]]/div/div/div/div[@role="combobox" and @tabindex="0"]'
        DropdownUtils.__selectSearchDropdownValueByXpath(wait, xpath, value)

    @staticmethod
    def selectValueByDropdownWrapperComponent(
        wait: WebDriverWait, component: WebElement, value: str
    ):
        xpath = f'./div/div[@role="combobox" and @tabindex="0"]'
        combobox = component.find_element(By.XPATH, xpath)
        DropdownUtils.selectDropdownValueByComponent(wait, combobox, value)
        return combobox
