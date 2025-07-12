from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver


class LinkUtils:
    
    """
    Utility class for interacting with link components in Appian UI.

        Usage Example:

        # Click a link with a specific label
        from robo_appian.components.LinkUtils import LinkUtils
        LinkUtils.click(wait, "Learn More")

    """
    @staticmethod
    def find(wait: WebDriverWait, label: str):
        xpath = f'.//a[normalize-space(text())="{label}"]'
        component = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
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
        
        component = LinkUtils.find(wait. label)
        component.click()
        return component
