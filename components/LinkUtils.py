from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


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
        xpath = f'.//a[normalize-space(text())="{label}"]'
        try:
            component = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        except TimeoutError as e:
            raise TimeoutError(f"Could not find clickable link with label '{label}': {e}")
        except Exception as e:
            raise Exception(f"Could not find clickable link with label '{label}': {e}")
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
        component.click()
        return component
