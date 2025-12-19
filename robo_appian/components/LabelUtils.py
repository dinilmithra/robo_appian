from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from robo_appian.utils.ComponentUtils import ComponentUtils


class LabelUtils:
    """
    Utility class for interacting with label components in Appian UI.
    Usage Example:
        # Find a label by its text
        component = LabelUtils._findByLabelText(wait, "Submit")
        # Click a label by its text
        LabelUtils.clickByLabelText(wait, "Submit")
    """

    @staticmethod
    def __findByLabelText(wait: WebDriverWait, label: str):
        """
        Finds a label element by its text.

        :param wait: Selenium WebDriverWait instance.
        :param label: The text of the label to find.
        :return: WebElement representing the label.
        Example:
            component = LabelUtils._findByLabelText(wait, "Submit")
        """
        xpath = f'//*[normalize-space(translate(., "\u00a0", " "))="{label}"]'
        try:
            # component = wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
            component = ComponentUtils.waitForComponentToBeVisibleByXpath(wait, xpath)
        except Exception as e:
            raise Exception(f"Label with text '{label}' not found.") from e

        return component

    @staticmethod
    def clickByLabelText(wait: WebDriverWait, label: str):
        """
        Clicks a label element identified by its text.

        :param wait: Selenium WebDriverWait instance.
        :param label: The text of the label to click.
        Example:
            LabelUtils.clickByLabelText(wait, "Submit")
        """
        component = LabelUtils.__findByLabelText(wait, label)
        ComponentUtils.click(wait, component)

    @staticmethod
    def isLabelExists(wait: WebDriverWait, label: str):
        try:
            LabelUtils.__findByLabelText(wait, label)
        except Exception:
            return False
        return True

    @staticmethod
    def isLabelExistsAfterLoad(wait: WebDriverWait, label: str):
        try:
            xpath = f'.//*[normalize-space(translate(., "\u00a0", " "))="{label}"]'
            wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
        except Exception:
            return False
        return True
