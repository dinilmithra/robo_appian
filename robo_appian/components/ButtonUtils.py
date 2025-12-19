from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from robo_appian.utils.ComponentUtils import ComponentUtils


class ButtonUtils:
    """
    Utility class for interacting with button components in Appian UI.
    Usage Example:
        # Click a button by its label
        from robo_appian.components.ButtonUtils import ButtonUtils
        ButtonUtils.clickByLabelText(wait, "Submit")
    """

    @staticmethod
    def _findByPartialLabelText(wait: WebDriverWait, label: str):
        """
        Finds a button by its label.

        Parameters:
            wait: Selenium WebDriverWait instance.
            label: The label of the button to find.

        Returns:
            WebElement representing the button.

        Example:
            component = ButtonUtils._findByPartialLabelText(wait, "Submit")
        """
        xpath = f"//button[./span[contains(translate(normalize-space(.), '\u00a0', ' '), '{label}')]]"
        try:
            component = ComponentUtils.waitForComponentToBeVisibleByXpath(wait, xpath)
        except Exception as e:
            raise Exception(
                f"Button with label '{label}' not found or not clickable."
            ) from e
        return component

    @staticmethod
    def __findByLabelText(wait: WebDriverWait, label: str):
        xpath = f".//button[./span[normalize-space(.)='{label}']]"
        try:
            component = ComponentUtils.waitForComponentToBeVisibleByXpath(wait, xpath)
        except Exception as e:
            raise Exception(f"Button with label '{label}' not found.") from e
        return component

    @staticmethod
    def clickByPartialLabelText(wait: WebDriverWait, label: str):
        """Finds a button by its partial label and clicks it.

        Parameters:
            wait: Selenium WebDriverWait instance.
            label: The partial label of the button to click.
            Example:
                ButtonUtils.clickByPartialLabelText(wait, "Button Label")
        """
        component = ButtonUtils._findByPartialLabelText(wait, label)

        ComponentUtils.click(wait, component)

    @staticmethod
    def clickByLabelText(wait: WebDriverWait, label: str):
        """Finds a button by its label and clicks it.

        Parameters:
            wait: Selenium WebDriverWait instance.
            label: The label of the button to click.
            Example:
                ButtonUtils.clickByLabelText(wait, "Button Label")
        """
        component = ButtonUtils.__findByLabelText(wait, label)

        ComponentUtils.click(wait, component)

    @staticmethod
    def clickById(wait: WebDriverWait, id: str):
        """
        Finds and clicks an input button by its HTML id attribute.

        Parameters:
            wait: Selenium WebDriverWait instance.
            id: The HTML id of the input button.

        Example:
            ButtonUtils.clickById(wait, "button_id")

        """
        try:
            component = wait.until(EC.element_to_be_clickable((By.ID, id)))
        except Exception as e:
            raise Exception(
                f"Input button with id '{id}' not found or not clickable."
            ) from e

        ComponentUtils.click(wait, component)

    @staticmethod
    def isButtonExistsByLabelText(wait: WebDriverWait, label: str):
        xpath = f".//button[./span[normalize-space(.)='{label}']]"
        try:
            ComponentUtils.findComponentByXPath(wait, xpath)
        except Exception:
            return False
        return True

    @staticmethod
    def isButtonExistsByPartialLabelText(wait: WebDriverWait, label: str):
        xpath = f".//button[./span[contains(translate(normalize-space(.), '\u00a0', ' '), '{label}')]]"
        try:
            ComponentUtils.findComponentByXPath(wait, xpath)
        except Exception:
            return False
        return True

    @staticmethod
    def isButtonExistsByPartialLabelTextAfterLoad(wait: WebDriverWait, label: str):
        try:
            ButtonUtils._findByPartialLabelText(wait, label)
        except Exception:
            return False
        return True

    @staticmethod
    def waitForButtonToBeVisibleByPartialLabelText(wait: WebDriverWait, label: str):
        xpath = f".//button[./span[contains(translate(normalize-space(.), '\u00a0', ' '), '{label}')]]"
        try:
            component = ComponentUtils.waitForComponentToBeVisibleByXpath(wait, xpath)
        except Exception as e:
            raise Exception(f"Button with partial label '{label}' not visible.") from e
        return component
