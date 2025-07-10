from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class ButtonUtils():
    """
    Utility class for interacting with button elements in Selenium-based Appian UI automation.
    
        Usage Example:      

        from selenium.webdriver.support.ui import WebDriverWait
        from robo_appian.utils.components.ButtonUtils import ButtonUtils

        wait = WebDriverWait(driver, 10)
        ButtonUtils.click(wait, "Login")

    """

    @staticmethod
    def find(wait, label):
        """
        Finds a button element by its label.

        Parameters:
            wait: Selenium WebDriverWait instance.
            label: The visible text label of the button.

        Returns:
            The Selenium WebElement for the button.

        Example:
            ButtonUtils.find(wait, "Submit")

        """

        # This method locates a button that contains a span with the specified label text.

        xpath = f".//button[./span[contains(translate(normalize-space(.), '\u00A0', ' '), '{label}')]]"
        component = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        return component

    @staticmethod
    def click(wait, label):
        """
        Clicks a button identified by its label.

        Parameters:
            wait: Selenium WebDriverWait instance.
            label: The visible text label of the button.
        Example:
            ButtonUtils.click(wait, "Submit")

        """
        component = ButtonUtils.find(wait, label)
        component.click()

    @staticmethod
    def clickInputButtonById(wait, id):
        """
        Finds and clicks an input button by its HTML id attribute.

        Parameters:
            wait: Selenium WebDriverWait instance.
            id: The HTML id of the input button.

        Example:
            ButtonUtils.clickInputButtonById(wait, "button_id")

        """
        component = wait.until(EC.element_to_be_clickable((By.ID, id)))
        component.click()
