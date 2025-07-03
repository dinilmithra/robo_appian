from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class LinkUtils():

    @staticmethod
    def click(wait, label):
        xpath = f'.//p/span[text()="{label}"]'
        # component = wait.until(EC.presence_of_element_located((By.XPATH, xpath)) )
        component = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        component.click()
        return component
