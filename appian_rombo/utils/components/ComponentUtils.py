from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC


class ComponentUtils():

    @staticmethod
    def today():
        from datetime import date
        today = date.today()
        yesterday_formatted = today.strftime("%m/%d/%Y")
        return yesterday_formatted

    @staticmethod
    def yesterday():
        from datetime import date, timedelta
        yesterday = date.today() - timedelta(days=1)
        yesterday_formatted = yesterday.strftime("%m/%d/%Y")
        return yesterday_formatted

    @staticmethod
    def find_dropdown_id(wait, dropdown_label):
        label_class_name = "FieldLayout---field_label"
        xpath = f'.//div/span[normalize-space(text())="{dropdown_label}" and @class="{label_class_name}"]'
        span_element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        span_element_id = span_element.get_attribute('id')
        return span_element_id

    @staticmethod
    def find_input_id(wait, label_text):
        label_class_name = "FieldLayout---field_label"
        xpath = f'.//div/div/label[@class="{label_class_name}" and contains(normalize-space(text()), "{label_text}")]'
        label_element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        input_element_id = label_element.get_attribute('for')
        return input_element_id

    @staticmethod
    def set_input_value(wait, label_text, value):
        input_element_id = ComponentUtils.find_input_id(wait, label_text)
        input_element = ComponentUtils.set_input_value_using_id(wait, input_element_id, value)
        return input_element

    @staticmethod
    def set_input_value_using_id(wait, input_element_id, value):
        input_element = wait.until(EC.presence_of_element_located((By.ID, input_element_id)))
        input_element = wait.until(EC.element_to_be_clickable((By.ID, input_element_id)))
        input_element.clear()
        input_element.send_keys(value)
        input_element.send_keys(Keys.RETURN)
        return input_element

    @staticmethod
    def select_search_dropdown_value(wait, label, value):
        span_element_id = ComponentUtils.find_dropdown_id(wait, label)
        xpath = f'.//div[@id="{span_element_id}_value"]'
        combobox = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        disabled = combobox.get_attribute("aria-disabled")
        if disabled == "true":
            return
        aria_controls = combobox.get_attribute("aria-controls")
        combobox = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        combobox.click()

        input_element_id = span_element_id + "_searchInput"
        ComponentUtils.set_input_value_using_id(wait, input_element_id, value)

        xpath = f'.//ul[@id="{aria_controls}"]/li[./div[normalize-space(text())="{value}"]]'
        component = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        component.click()

    @staticmethod
    def selectDropdownValue(wait, combobox, value):

        aria_controls = combobox.get_attribute("aria-controls")
        combobox.click()

        xpath = f'.//div/ul[@id="{aria_controls}"]/li[./div[normalize-space(text())="{value}"]]'
        component = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        component = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        component.click()

    @staticmethod
    def select_dropdown_value(wait, label, value):
        span_element_id = ComponentUtils.find_dropdown_id(wait, label)

        xpath = f'.//div[@id="{span_element_id}_value"]'
        combobox = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        disabled = combobox.get_attribute("aria-disabled")
        if disabled == "true":
            return

        combobox = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        ComponentUtils.selectDropdownValue(wait, combobox, value)

    @staticmethod
    def findButton(wait, button_text):
        xpath = f'.//button[.//span/span[contains(normalize-space(text()), "{button_text}")]]'
        component = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        return component

    @staticmethod
    def click_button(wait, button_text):
        component = ComponentUtils.findButton(wait, button_text)
        component.click()

    @staticmethod
    def select_tab(wait, tab_label_text):
        xpath = f'.//div[@role="presentation"]/div/div/p[./span[normalize-space(text())="{tab_label_text}"]]'
        component = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        component.click()

    @staticmethod
    def findSuccessMessage(wait, message):
        xpath = f'.//div/div/p/span/strong[normalize-space(text())="{message}"]'
        component = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        return component

    @staticmethod
    def findComponentUsingXpathAndClick(wait, xpath):
        component = ComponentUtils.findComponentUsingXpath(wait, xpath)
        component.click()

    @staticmethod
    def findComponentUsingXpath(wait, xpath):
        component = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        return component

    @staticmethod
    def checkComponentExistsByXpath(wait, xpath):
        status = False
        try:
            component = ComponentUtils.findComponentUsingXpath(wait, xpath)
            status = True
        except NoSuchElementException:
            pass

        return status

    @staticmethod
    def checkComponentExistsById(driver, id):
        status = False
        try:
            component = driver.find_element(By.ID, id)
            status = True
        except NoSuchElementException:
            pass

        return status

    @staticmethod
    def findCount(wait, xpath):

        length = 0

        try:
            component = wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath)))
            length = len(component)
        except NoSuchElementException:
            pass

        return length

    @staticmethod
    def findComponent(wait, label):
        xpath = f".//div/label[text()='{label}']"
        component = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        component_id = component.get_attribute("for")

        component = wait.until(EC.element_to_be_clickable((By.ID, component_id)))
        return component
    
    @staticmethod
    def tab(driver):
        actions = ActionChains(driver)
        actions.send_keys(Keys.TAB).perform()