from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC


class InputUtils():

    @staticmethod
    def findComponent(wait, label):
        xpath = f".//div/label[text()='{label}']"
        component = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        component_id = component.get_attribute("for")
        component = wait.until(EC.element_to_be_clickable((By.ID, component_id)))
        return component

    @staticmethod
    def setValueUsingComponent(component, value):
        component.clear()
        component.send_keys(value)
        return component

    @staticmethod
    def setValueAndSubmitUsingComponent(component, value):
        component = InputUtils.setValueUsingComponent(component, value)
        component.send_keys(Keys.ENTER)
        return component

    @staticmethod
    def setInputValue(wait, label, value):
        component = InputUtils.findComponent(wait, label)
        InputUtils.setValueUsingComponent(component, value)
        return component

    @staticmethod
    def setValueAndSubmit(wait, label, value):
        component = InputUtils.findComponent(wait, label)
        component = InputUtils.setValueAndSubmitUsingComponent(component, value)
        return component

    @staticmethod
    def setSearchInputValue(wait, label, value):
        xpath = f".//div[./div/span[text()='{label}']]/div/div/div/input[@role='combobox']"
        search_input_component = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        aria_controls = search_input_component.get_attribute("aria-controls")
        InputUtils.setValueUsingComponent(search_input_component, value)

        xpath = f".//ul[@id='{aria_controls}' and @role='listbox' ]/li[@role='option']/div/div/div/div/div/div/p[text()='{value}'][1]"
        drop_down_item = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        drop_down_item.click()
