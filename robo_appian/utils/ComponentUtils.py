import tomllib
from pathlib import Path
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait


class ComponentUtils:

    @staticmethod
    def get_version():
        try:
            toml_path = Path(__file__).parent.parent / "pyproject.toml"
            with open(toml_path, "rb") as f:
                data = tomllib.load(f)
                return data.get("project", {}).get("version", "0.0.0")
        except Exception:
            return "0.0.0"

    @staticmethod
    def today():
        """
        Returns today's date formatted as MM/DD/YYYY.
        """

        from datetime import date

        today = date.today()
        yesterday_formatted = today.strftime("%m/%d/%Y")
        return yesterday_formatted

    @staticmethod
    def yesterday():
        """
        Returns yesterday's date formatted as MM/DD/YYYY.
        """

        from datetime import date, timedelta

        yesterday = date.today() - timedelta(days=1)
        yesterday_formatted = yesterday.strftime("%m/%d/%Y")
        return yesterday_formatted

    @staticmethod
    def findChildComponentByXpath(
        wait: WebDriverWait, component: WebElement, xpath: str
    ):
        """Finds a child component using the given XPath within a parent component.

        :param wait: WebDriverWait instance to wait for elements
        :param component: Parent WebElement to search within
        :param xpath: XPath string to locate the child component
        :return: WebElement if found, raises NoSuchElementException otherwise
        Example usage:
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium import webdriver

        driver = webdriver.Chrome()
        wait = WebDriverWait(driver, 10)
        parent_component = driver.find_element(By.ID, "parent")
        xpath = ".//button[@class='child']"
        child_component = ComponentUtils.findChildComponentByXpath(wait, parent_component, xpath)
        """
        try:
            component = wait.until(lambda comp: component.find_element(By.XPATH, xpath))
        except Exception as e:
            raise Exception(
                f"Child component with XPath '{xpath}' not found within the given parent component."
            ) from e
        return component

    @staticmethod
    def findComponentById(wait: WebDriverWait, id: str):
        try:
            component = wait.until(EC.presence_of_element_located((By.ID, id)))
        except Exception as e:
            raise Exception(f"Component with ID '{id}' not found.") from e
        return component

    @staticmethod
    def waitForComponentToBeVisibleByXpath(wait: WebDriverWait, xpath: str):
        try:
            component = wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
        except Exception as e:
            raise Exception(f"Component with XPath '{xpath}' not visible.") from e
        return component

    @staticmethod
    def waitForComponentNotToBeVisibleByXpath(wait: WebDriverWait, xpath: str):
        """
        Wait until the element identified by the given XPath is no longer visible.
        This function uses the provided WebDriverWait instance to poll for the
        invisibility (or absence) of the element located by the given XPath.
        The behavior (timeout and polling interval) is determined by the
        configuration of the supplied WebDriverWait.
        Parameters
        ----------
        wait : selenium.webdriver.support.wait.WebDriverWait
            A WebDriverWait instance configured with the desired timeout and polling settings.
        xpath : str
            The XPath expression used to locate the target element.
        Returns
        -------
        bool
            True if the element became invisible or was removed from the DOM before the wait timed out.
        Raises
        ------
        Exception
            If the element does not become invisible within the wait timeout or another error occurs while waiting.
        """
        try:
            return wait.until(EC.invisibility_of_element_located((By.XPATH, xpath)))
        except Exception as e:
            raise Exception(f"Component with XPath '{xpath}' is still visible.") from e

    # @staticmethod
    # def waitForComponentToBeVisibleByXpath(wait: WebDriverWait, xpath: str):
    #     """
    #     Finds a component using the given XPath in the current WebDriver instance.

    #         :param wait: WebDriverWait instance to wait for elements
    #         :param xpath: XPath string to locate the component
    #         :return: WebElement if found, raises NoSuchElementException otherwise

    #     Example usage:
    #         component = ComponentUtils.waitForComponentToBeVisibleByXpath(wait, "//button[@id='submit']")
    #         component.click()
    #     """
    #     try:
    #         component = wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
    #     except Exception:
    #         raise Exception(f"Component with XPath '{xpath}' not visible.")
    #     return component

    @staticmethod
    def checkComponentExistsByXpath(wait: WebDriverWait, xpath: str):
        """Checks if a component with the given XPath exists in the current WebDriver instance."""
        status = False
        try:
            ComponentUtils.waitForComponentToBeVisibleByXpath(wait, xpath)
            status = True
        except NoSuchElementException:
            pass

        return status

    @staticmethod
    def checkComponentExistsById(driver: WebDriver, id: str):
        """Checks if a component with the given ID exists in the current WebDriver instance.

        :param driver: WebDriver instance to check for the component
        :param id: ID of the component to check
        :return: True if the component exists, False otherwise
        Example usage:
        exists = ComponentUtils.checkComponentExistsById(driver, "submit-button")
        print(f"Component exists: {exists}")
        """
        status = False
        try:
            driver.find_element(By.ID, id)
            status = True
        except NoSuchElementException:
            pass

        return status

    @staticmethod
    def findCount(wait: WebDriverWait, xpath: str):
        """Finds the count of components matching the given XPath.

        :param wait: WebDriverWait instance to wait for elements
        :param xpath: XPath string to locate components
        :return: Count of components matching the XPath
        Example usage:
        count = ComponentUtils.findCount(wait, "//div[@class='item']")
        print(f"Number of items found: {count}")
        """

        length = 0

        try:
            component = wait.until(
                EC.presence_of_all_elements_located((By.XPATH, xpath))
            )
            length = len(component)
        except NoSuchElementException:
            pass

        return length

    @staticmethod
    def tab(wait: WebDriverWait):
        """Simulates a tab key press in the current WebDriver instance.

        :param wait: WebDriverWait instance to wait for elements
        :return: None
        Example usage:
        ComponentUtils.tab(wait)
        """
        driver = wait._driver
        actions = ActionChains(driver)
        actions.send_keys(Keys.TAB).perform()

    @staticmethod
    def findComponentsByXPath(wait: WebDriverWait, xpath: str):
        """Finds all components matching the given XPath and returns a list of valid components
        that are clickable and displayed.

        :param wait: WebDriverWait instance to wait for elements
        :param xpath: XPath string to locate components
        :return: List of valid WebElement components
        Example usage:
        components = ComponentUtils.findComponentsByXPath(wait, "//button[@class='submit']")
        for component in components:
            component.click()
        """
        # Wait for the presence of elements matching the XPath
        wait.until(EC.presence_of_element_located((By.XPATH, xpath)))

        # Find all matching elements
        driver = wait._driver
        components = driver.find_elements(By.XPATH, xpath)

        # Filter for clickable and displayed components
        valid_components = []
        for component in components:
            try:
                if component.is_displayed() and component.is_enabled():
                    valid_components.append(component)
            except Exception:
                continue

        if len(valid_components) > 0:
            return valid_components

        raise Exception(f"No valid components found for XPath: {xpath}")

    @staticmethod
    def findComponentByXPath(wait: WebDriverWait, xpath: str):

        try:
            component = wait._driver.find_element(By.XPATH, xpath)
        except NoSuchElementException as e:
            raise Exception(f"Component with XPath '{xpath}' not found.") from e
        return component

    @staticmethod
    def findComponentUsingXpathAndClick(wait: WebDriverWait, xpath: str):
        """Finds a component using the given XPath and clicks it.

        :param wait: WebDriverWait instance to wait for elements
        :param xpath: XPath string to locate the component
        :return: None
        Example usage:
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium import webdriver

        driver = webdriver.Chrome()
        wait = WebDriverWait(driver, 10)
        xpath = "//button[@id='submit']"
        ComponentUtils.findComponentUsingXpathAndClick(wait, xpath)
        """

        component = ComponentUtils.waitForComponentToBeVisibleByXpath(wait, xpath)
        ComponentUtils.click(wait, component)

    @staticmethod
    def click(wait: WebDriverWait, component: WebElement):
        """
        Clicks the given component after waiting for it to be clickable.

            :param wait: WebDriverWait instance to wait for elements
            :param component: WebElement representing the component to click
            :return: None
        Example usage:
            ComponentUtils.click(wait, component)
        """
        wait.until(EC.element_to_be_clickable(component))
        actions = ActionChains(wait._driver)
        actions.move_to_element(component).click().perform()

    @staticmethod
    def waitForComponentToBeInVisible(wait: WebDriverWait, component: WebElement):
        try:
            wait.until(EC.staleness_of(component))
        except Exception as e:
            raise Exception(
                "Component did not become invisible (stale) within the timeout period."
            ) from e

    @staticmethod
    def isComponentPresentByXpath(wait: WebDriverWait, xpath: str):
        status = False
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            status = True
        except NoSuchElementException:
            pass

        return status

    @staticmethod
    def waitForElementToBeVisibleById(wait: WebDriverWait, id: str):
        return wait.until(EC.visibility_of_element_located((By.ID, id)))

    @staticmethod
    def waitForElementNotToBeVisibleById(wait: WebDriverWait, id: str):
        return wait.until(EC.invisibility_of_element_located((By.ID, id)))

    @staticmethod
    def waitForElementToBeVisibleByText(wait: WebDriverWait, text: str):
        xpath = f'//*[normalize-space(translate(., "\u00a0", " "))="{text}" and not(*[normalize-space(translate(., "\u00a0", " "))="{text}"]) and not(ancestor-or-self::*[contains(@class, "---hidden")])]'
        return wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))

    @staticmethod
    def waitForElementNotToBeVisibleByText(wait: WebDriverWait, text: str):
        xpath = f'//*[normalize-space(translate(., "\u00a0", " "))="{text}" and not(*[normalize-space(translate(., "\u00a0", " "))="{text}"]) and not(ancestor-or-self::*[contains(@class, "---hidden")])]'
        return wait.until(EC.invisibility_of_element_located((By.XPATH, xpath)))

    @staticmethod
    def waitForComponentToBeClickableByXpath(
        wait: WebDriverWait, component: WebElement
    ):
        try:
            return wait.until(EC.element_to_be_clickable(component))
        except Exception as e:
            raise Exception(
                "Component did not become clickable within the timeout period. "
            ) from e
