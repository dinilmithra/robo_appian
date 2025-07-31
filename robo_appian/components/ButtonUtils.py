from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class ButtonUtils:
    @staticmethod
    def find(wait: WebDriverWait, label: str):
        xpath = f".//button[./span[contains(translate(normalize-space(.), '\u00a0', ' '), '{label}')]]"
        try:
            component = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        except Exception as e:
            raise RuntimeError(f"Button with label '{label}' not found or not clickable.") from e
        return component

    @staticmethod
    def click(wait: WebDriverWait, label: str):
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
    def clickInputButtonById(wait: WebDriverWait, id: str):
        """
        Finds and clicks an input button by its HTML id attribute.

        Parameters:
            wait: Selenium WebDriverWait instance.
            id: The HTML id of the input button.

        Example:
            ButtonUtils.clickInputButtonById(wait, "button_id")

        """
        try:
            component = wait.until(EC.element_to_be_clickable((By.ID, id)))
        except TimeoutError as e:
            raise TimeoutError(f"Input button with id '{id}' not found or not clickable.") from e
        except Exception as e:
            raise RuntimeError(f"Input button with id '{id}' not found or not clickable.") from e

        component.click()
