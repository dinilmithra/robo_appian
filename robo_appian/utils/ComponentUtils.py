from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait


class ComponentUtils:
    """
    Utility class for interacting with various components in Appian UI.

    """

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
    def findSuccessMessage(wait: WebDriverWait, message: str):
        """
        Finds a success message in the UI by its text.
        Parameters:
            wait: Selenium WebDriverWait instance.
            message: The text of the success message to find.
        Returns:
            The Selenium WebElement for the success message.
        Example:
            ComponentUtils.findSuccessMessage(wait, "Operation completed successfully")
        """
        # This method locates a success message that contains a strong tag with the specified text.
        # The message is normalized to handle any extra spaces.
        # It uses the presence_of_element_located condition to ensure the element is present in the DOM.

        xpath = f'.//div/div/p/span/strong[normalize-space(text())="{message}"]'
        component = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        return component

    @staticmethod
    def findComponentUsingXpathAndClick(wait: WebDriverWait, xpath: str):
        """
        Finds a component using its XPath and clicks it.
        Parameters:
            wait: Selenium WebDriverWait instance.
            xpath: The XPath of the component to find and click.
        Example:
            ComponentUtils.findComponentUsingXpathAndClick(wait, "//button[@id='submit']")

        """
        # This method locates a component using the provided XPath and clicks it.
        # It uses the presence_of_element_located condition to ensure the element is present in the DOM.
        # After locating the component, it clicks it to perform the action.
        component = ComponentUtils.findComponentUsingXpath(wait, xpath)
        component.click()

    @staticmethod
    def findComponentUsingXpath(wait: WebDriverWait, xpath: str):
        """
        Finds a component using its XPath.
        Parameters:
            wait: Selenium WebDriverWait instance.
            xpath: The XPath of the component to find.
        Returns:
            The Selenium WebElement for the component.
        Example:
            ComponentUtils.findComponentUsingXpath(wait, "//button[@id='submit']")
        """
        # This method locates a component using the provided XPath.
        # It uses the presence_of_element_located condition to ensure the element is present in the DOM.
        # The method returns the WebElement for further interaction.
        component = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        return component

    @staticmethod
    def checkComponentExistsByXpath(wait: WebDriverWait, xpath: str):
        """
        Checks if a component exists using its XPath.
        Parameters:
            wait: Selenium WebDriverWait instance.
            xpath: The XPath of the component to check.
        Returns:
            True if the component exists, False otherwise.
        Example:
            ComponentUtils.checkComponentExistsByXpath(wait, "//button[@id='submit']")
        """
        # This method checks if a component exists by attempting to find it using the provided XPath.
        # If the component is found, it returns True; otherwise, it catches the NoSuchElementException and returns False.
        # It uses the presence_of_element_located condition to ensure the element is present in the DOM.

        status = False
        try:
            ComponentUtils.findComponentUsingXpath(wait, xpath)
            status = True
        except NoSuchElementException:
            pass

        return status

    @staticmethod
    def checkComponentExistsById(driver: WebDriver, id: str):
        """
        Checks if a component exists using its ID.
        Parameters:
            driver: Selenium WebDriver instance.
            id: The ID of the component to check.
        Returns:
            True if the component exists, False otherwise.
        Example:
            ComponentUtils.checkComponentExistsById(driver, "submit-button")
        """
        # This method checks if a component exists by attempting to find it using the provided ID.
        # If the component is found, it returns True; otherwise, it catches the NoSuchElementException and returns False.
        # It uses the find_element method to locate the element by its ID.

        status = False
        try:
            driver.find_element(By.ID, id)
            status = True
        except NoSuchElementException:
            pass

        return status

    @staticmethod
    def findCount(wait: WebDriverWait, xpath: str):
        """
        Finds the count of components matching the given XPath.
        Parameters:
            wait: Selenium WebDriverWait instance.
            xpath: The XPath of the components to count.
        Returns:
            The count of components matching the XPath.
        Example:
            count = ComponentUtils.findCount(wait, "//div[@class='item']")
        """
        # This method locates all components matching the provided XPath and returns their count.
        # It uses the presence_of_all_elements_located condition to ensure all elements are present in the DOM.
        # If no elements are found, it catches the NoSuchElementException and returns 0.

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
    def tab(driver: WebDriver):
        """
        Simulates a TAB key press in the browser.

        Parameters:
            driver: Selenium WebDriver instance.
        Example:
            ComponentUtils.tab(driver)
        """
        # This method simulates a TAB key press in the browser using ActionChains.
        # It creates an ActionChains instance, sends the TAB key, and performs the action.
        # This is useful for navigating through form fields or components in the UI.
        # It uses the ActionChains class to perform the key press action.

        actions = ActionChains(driver)
        actions.send_keys(Keys.TAB).perform()

    @staticmethod
    def findComponentsByXPath(wait: WebDriverWait, xpath: str):
        """
        Finds multiple components that match the same XPath.

        Parameters:
            wait: Selenium WebDriverWait instance.
            xpath: The XPath expression to find components.

        Returns:
            List of WebElement objects that match the XPath.

        Raises:
            Exception: If no components are found.
        """
        
        # Wait for at least one element to be present
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
