from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver


class LabelUtils:
    """
    Utility class for interacting with label components in Appian UI.

        Usage Example:

        # Find a label component
        from robo_appian.components.LabelUtils import LabelUtils
        label_component = LabelUtils.find(wait, "Username")

    """

    @staticmethod
    def find(wait : WebDriverWait, label: str):
        """
        Finds a label component by its text.

        Parameters:
            wait: Selenium WebDriverWait instance.
            label: The visible text label of the component.

        Returns:
            The Selenium WebElement for the label component.

        Example:
            LabelUtils.find(wait, "Username")

        """
        # This method locates a label component that contains the specified text.
        # It uses XPath to find the element that matches the text.

        xpath = f".//*[text()='{label}']"
        component = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        return component
