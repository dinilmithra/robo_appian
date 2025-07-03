from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class ButtonUtils():

    @staticmethod
    def find(wait, label):
        xpath = f".//button[./span[contains(translate(normalize-space(.), '\u00A0', ' '), '{label}')]]"
        component = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        return component

    @staticmethod
    def click(wait, label):
        component = ButtonUtils.find(wait, label)
        component.click()

    @staticmethod
    def clickInputButtonById(wait, id):
        component = wait.until(EC.element_to_be_clickable((By.ID, id)))
        component.click()
