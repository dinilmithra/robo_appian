from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from robo_appian.utils.ComponentUtils import ComponentUtils


class TabUtils:
    """
    Utility class for handling tab components in a web application using Selenium.
    Example usage:
        from selenium import webdriver
        from selenium.webdriver.support.ui import WebDriverWait
        from robo_appian.components.TabUtils import TabUtils

        driver = webdriver.Chrome()
        wait = WebDriverWait(driver, 10)

        # Find a selected tab by its label
        selected_tab = TabUtils.findSelectedTabByLabelText(wait, "Tab Label")

        # Select an inactive tab by its label
        TabUtils.selectTabByLabelText(wait, "Inactive Tab Label")

        driver.quit()
    """

    @staticmethod
    def findTabByLabelText(wait: WebDriverWait, label: str) -> WebElement:
        xpath = f'//div/div[@role="link" ]/div/div/div/div/div/p[normalize-space(.)="{label}"]'
        try:
            component = wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
        except Exception as e:
            raise Exception(f"Tab with label '{label}' not found.") from e
        return component

    @staticmethod
    def selectTabByLabelText(wait: WebDriverWait, label: str):
        component = TabUtils.findTabByLabelText(wait, label)
        ComponentUtils.click(wait, component)

    @staticmethod
    def checkTabSelectedByLabelText(wait: WebDriverWait, label: str):
        component = TabUtils.findTabByLabelText(wait, label)

        select_text = "Selected Tab."
        xpath = f'./span[normalize-space(.)="{select_text}"]'
        try:
            component = ComponentUtils.findChildComponentByXpath(wait, component, xpath)
        except Exception:
            return False

        return True
