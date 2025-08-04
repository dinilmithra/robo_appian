from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


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
        TabUtils.selectInactiveTabByLabelText(wait, "Inactive Tab Label")

        driver.quit()
    """

    @staticmethod
    def findSelectedTabByLabelText(wait, label):
        """
        Finds the currently selected tab by its label.

        :param wait: Selenium WebDriverWait instance.
        :param label: The label of the tab to find.
        :return: WebElement representing the selected tab.
        Example:
            component = TabUtils.findSelectedTabByLabelText(wait, "Tab Label")
        """
        xpath = f".//div[./div[./div/div/div/div/div/p/strong[normalize-space(text())='{label}']]/span[text()='Selected Tab.']]/div[@role='link']"
        try:
            component = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        except TimeoutError as e:
            raise TimeoutError(f"Could not find selected tab with label '{label}': {e}")
        except Exception as e:
            raise RuntimeError(f"Could not find selected tab with label '{label}': {e}")
        return component

    @staticmethod
    def selectInactiveTabByLabelText(wait, label):
        """
        Selects an inactive tab by its label.

        :param wait: Selenium WebDriverWait instance.
        :param label: The label of the tab to select.
        :return: None
        Example:
            TabUtils.selectInactiveTabByLabelText(wait, "Tab Label")
        """
        xpath = f".//div[@role='link']/div/div/div/div/div[./p/span[text()='{label}']]"
        try:
            component = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        except TimeoutError as e:
            raise TimeoutError(f"Could not find tab with label '{label}': {e}")
        except Exception as e:
            raise RuntimeError(f"Could not find tab with label '{label}': {e}")
        component.click()
