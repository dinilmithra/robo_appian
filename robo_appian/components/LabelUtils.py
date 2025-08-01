from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class LabelUtils:
    """
    Utility class for interacting with label components in Appian UI.
    Usage Example:
        # Find a label by its text
        component = LabelUtils.findByLabelText(wait, "Submit")
        # Click a label by its text
        LabelUtils.clickByLabelText(wait, "Submit")
    """

    @staticmethod
    def findByLabelText(wait: WebDriverWait, label: str):
        """
        Finds a label element by its text.

        :param wait: Selenium WebDriverWait instance.
        :param label: The text of the label to find.
        :return: WebElement representing the label.
        Example:
            component = LabelUtils.findByLabelText(wait, "Submit")
        """
        xpath = f".//*[normalize-space(text())='{label}']"
        try:
            component = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        except Exception as e:
            raise RuntimeError(f"Label with text '{label}' not found.") from e

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
        component = LabelUtils.findByLabelText(wait, label)
        component.click()
