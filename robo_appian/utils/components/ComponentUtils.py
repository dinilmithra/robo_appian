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

    # @staticmethod
    # def find_dropdown_id(wait, dropdown_label):
    #     label_class_name = "FieldLayout---field_label"
    #     xpath = f'.//div/span[normalize-space(text())="{dropdown_label}" and @class="{label_class_name}"]'
    #     span_element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
    #     span_element_id = span_element.get_attribute('id')
    #     return span_element_id

    # @staticmethod
    # def find_input_id(wait, label_text):
    #     label_class_name = "FieldLayout---field_label"
    #     xpath = f'.//div/div/label[@class="{label_class_name}" and contains(normalize-space(text()), "{label_text}")]'
    #     label_element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
    #     input_element_id = label_element.get_attribute('for')
    #     return input_element_id

    # @staticmethod
    # def set_input_value(wait, label_text, value):
    #     input_element_id = ComponentUtils.find_input_id(wait, label_text)
    #     input_element = ComponentUtils.set_input_value_using_id(wait, input_element_id, value)
    #     return input_element

    # @staticmethod
    # def set_input_value_using_id(wait, input_element_id, value):
    #     input_element = wait.until(EC.presence_of_element_located((By.ID, input_element_id)))
    #     input_element = wait.until(EC.element_to_be_clickable((By.ID, input_element_id)))
    #     input_element.clear()
    #     input_element.send_keys(value)
    #     input_element.send_keys(Keys.RETURN)
    #     return input_element

    # @staticmethod
    # def select_search_dropdown_value(wait, label, value):
    #     span_element_id = ComponentUtils.find_dropdown_id(wait, label)
    #     xpath = f'.//div[@id="{span_element_id}_value"]'
    #     combobox = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
    #     disabled = combobox.get_attribute("aria-disabled")
    #     if disabled == "true":
    #         return
    #     aria_controls = combobox.get_attribute("aria-controls")
    #     combobox = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
    #     combobox.click()

    #     input_element_id = span_element_id + "_searchInput"
    #     ComponentUtils.set_input_value_using_id(wait, input_element_id, value)

    #     xpath = f'.//ul[@id="{aria_controls}"]/li[./div[normalize-space(text())="{value}"]]'
    #     component = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
    #     component.click()

    # @staticmethod
    # def selectDropdownValue(wait, combobox, value):

    #     aria_controls = combobox.get_attribute("aria-controls")
    #     combobox.click()

    #     xpath = f'.//div/ul[@id="{aria_controls}"]/li[./div[normalize-space(text())="{value}"]]'
    #     component = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
    #     component = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
    #     component.click()

    # @staticmethod
    # def select_dropdown_value(wait, label, value):
    #     span_element_id = ComponentUtils.find_dropdown_id(wait, label)

    #     xpath = f'.//div[@id="{span_element_id}_value"]'
    #     combobox = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
    #     disabled = combobox.get_attribute("aria-disabled")
    #     if disabled == "true":
    #         return

    #     combobox = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
    #     ComponentUtils.selectDropdownValue(wait, combobox, value)

    # @staticmethod
    # def findButton(wait, button_text):
    #     xpath = f'.//button[.//span/span[contains(normalize-space(text()), "{button_text}")]]'
    #     component = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
    #     return component

    # @staticmethod
    # def click_button(wait, button_text):
    #     component = ComponentUtils.findButton(wait, button_text)
    #     component.click()

    # @staticmethod
    # def select_tab(wait, tab_label_text):
    #     xpath = f'.//div[@role="presentation"]/div/div/p[./span[normalize-space(text())="{tab_label_text}"]]'
    #     component = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
    #     component.click()

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

    # @staticmethod
    # def findComponent(wait, label):
    #     xpath = f".//div/label[text()='{label}']"
    #     component = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
    #     component_id = component.get_attribute("for")

    #     component = wait.until(EC.element_to_be_clickable((By.ID, component_id)))
    #     return component

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
