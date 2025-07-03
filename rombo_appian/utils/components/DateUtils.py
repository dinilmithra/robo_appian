from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from rombo_appian.utils.components.InputUtils import InputUtils


class DateUtils():

    @staticmethod
    def findComponent(wait, label):
        xpath = f".//div/label[text()='{label}']"
        component = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        component_id = component.get_attribute("for")

        component = wait.until(EC.element_to_be_clickable((By.ID, component_id)))
        return component

    @staticmethod
    def setDateValue(wait, label, value):
        component = DateUtils.findComponent(wait, label)
        InputUtils.setValueUsingComponent(component, value)
        return component

    @staticmethod
    def setDateValueAndSubmit(wait, label, value):
        # component=DateUtils.setDateValue(wait, label, value)
        # component.send_keys(Keys.RETURN)

        component = DateUtils.findComponent(wait, label)
        InputUtils.setValueAndSubmitUsingComponent(component, value)

        return component

    @staticmethod
    def click(wait, label):
        component = DateUtils.findComponent(wait, label)
        component.click()

        return component
