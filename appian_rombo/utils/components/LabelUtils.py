from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class LabelUtils():

    @staticmethod
    def find(wait, label):
        xpath = f".//*[text()='{label}']"
        component = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        return component
