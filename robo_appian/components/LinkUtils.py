from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from robo_appian.utils.ComponentUtils import ComponentUtils


class LinkUtils:
    """
    Utility class for handling link operations in Selenium WebDriver.
    Example usage:
        from selenium import webdriver
        from selenium.webdriver.support.ui import WebDriverWait
        from robo_appian.components.LinkUtils import LinkUtils

        driver = webdriver.Chrome()
        wait = WebDriverWait(driver, 10)
        LinkUtils.click(wait, "Learn More")
        driver.quit()
    """

    @staticmethod
    def find(wait: WebDriverWait, label: str):
        # xpath = f'.//a[normalize-space(.)="{label}"]'
        xpath = f'.//a[normalize-space(.)="{label}" and not(ancestor::*[@aria-hidden="true"])]'
        try:
            component = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        except Exception as e:
            raise Exception(f"Could not find clickable link with label '{label}': {e}") from e
        return component

    @staticmethod
    def click(wait: WebDriverWait, label: str):
        """
        Clicks a link identified by its label.

        Parameters:
            wait: Selenium WebDriverWait instance.
            label: The visible text label of the link.

        Example:
            LinkUtils.click(wait, "Learn More")
        """

        component = LinkUtils.find(wait, label)
        ComponentUtils.click(wait, component)
        return component
