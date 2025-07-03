from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class TabUtils():

    @staticmethod
    def find_selected_tab(wait, label):
        xpath = f".//div[./div[./div/div/div/div/div/p/strong[normalize-space(text())='{label}']]/span[text()='Selected Tab.']]/div[@role='link']"
        component = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        return component

    @staticmethod
    def select_tab(wait, label):
        xpath = f".//div[@role='link']/div/div/div/div/div[./p/span[text()='{label}']]"
        # xpath=f".//div[./div[./div/div/div/div/div/p/strong[normalize-space(text())='{label}']]/span[text()='Selected Tab.']]/div[@role='link']"        
        component = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        component.click()
