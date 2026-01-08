from selenium.webdriver.support.ui import WebDriverWait
from robo_appian.components.InputUtils  import  InputUtils
from robo_appian.utils.ComponentUtils import ComponentUtils


class SearchInputUtils:
    """
    Utility class for handling search input operations in Selenium WebDriver.
    Example usage:
        from selenium import webdriver
        from selenium.webdriver.support.ui import WebDriverWait
        from robo_appian.components.SearchInputUtils import SearchInputUtils

        driver = webdriver.Chrome()
        wait = WebDriverWait(driver, 10)
        SearchInputUtils.selectSearchDropdownByLabelText(wait, "Search Label", "Value")
        driver.quit()
    """

    @staticmethod
    def __findSearchInputComponentsByLabelPathAndSelectValue(wait: WebDriverWait, xpath: str, value: str):
            
        search_input_component = ComponentUtils.waitForComponentToBeVisibleByXpath(wait, xpath)
        attribute: str = "aria-controls"
        dropdown_list_id = search_input_component.get_attribute(attribute)
        if dropdown_list_id:
            InputUtils._setValueByComponent(wait, search_input_component, value)
            xpath = f'.//ul[@id="{dropdown_list_id}" and @role="listbox" ]/li[@role="option" and @tabindex="-1" and ./div/div/div/div/div/div/p[normalize-space(.)="{value}"][1]]'
            try:
                drop_down_item = ComponentUtils.waitForComponentToBeVisibleByXpath(wait, xpath)
            except Exception as e:
                raise Exception(
                    f"Dropdown item with value '{value}' not found for component '{search_input_component.text}'."
                ) from e
            ComponentUtils.click(wait, drop_down_item)
        else:
            raise ValueError(
                f"Search input component with label '{search_input_component.text}' does not have 'aria-controls' attribute."
            )

        return search_input_component

    @staticmethod
    def __selectSearchInputComponentsByPartialLabelText(wait: WebDriverWait, label: str, value: str):
        xpath = f'.//div[./div/span[contains(normalize-space(.)="{label}"]]/div/div/div/input[@role="combobox"]'
        SearchInputUtils.__findSearchInputComponentsByLabelPathAndSelectValue(wait, xpath, value)

    @staticmethod
    def __selectSearchInputComponentsByLabelText(wait: WebDriverWait, label: str, value: str):
        xpath = f'.//div[./div/span[normalize-space(translate(., "\u00a0", " "))="{label}"]]/div/div/div/input[@role="combobox"]'
        SearchInputUtils.__findSearchInputComponentsByLabelPathAndSelectValue(wait, xpath, value)

    @staticmethod
    def selectSearchDropdownByLabelText(wait: WebDriverWait, label: str, value: str):
        SearchInputUtils.__selectSearchInputComponentsByLabelText(wait, label, value)

    @staticmethod
    def selectSearchDropdownByPartialLabelText(wait: WebDriverWait, label: str, value: str):
        SearchInputUtils.__selectSearchInputComponentsByPartialLabelText(wait, label, value)
