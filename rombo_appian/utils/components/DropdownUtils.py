from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from rombo_appian.utils.components.InputUtils import InputUtils


class DropdownUtils():

    @staticmethod
    def findDropdownEnabled(wait, dropdown_label):
        xpath = f'.//div[./div/span[normalize-space(text())="{dropdown_label}"]]/div/div/div/div[@role="combobox" and @tabindex="0"]'
        component = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        return component

    @staticmethod
    def selectValueUsingComponent(wait, combobox, value):
        component = combobox.find_element(By.XPATH, "./div/div")
        aria_controls = component.get_attribute("aria-controls")
        component.click()

        xpath = f'.//div/ul[@id="{aria_controls}"]/li[./div[normalize-space(text())="{value}"]]'
        # component = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        component = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        component.click()

    @staticmethod
    def selectDropdownValue(wait, label, value):
        combobox = DropdownUtils.findDropdownEnabled(wait, label)
        aria_controls = combobox.get_attribute("aria-controls")
        combobox.click()

        xpath = f'.//div/ul[@id="{aria_controls}"]/li[./div[normalize-space(text())="{value}"]]'
        component = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        component = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        component.click()

    @staticmethod
    def selectSearchDropdownValue(wait, dropdown_label, value):
        component = DropdownUtils.findDropdownEnabled(wait, dropdown_label)
        component_id = component.get_attribute("aria-labelledby")
        aria_controls = component.get_attribute("aria-controls")
        component.click()

        input_component_id = component_id + "_searchInput"
        input_component = wait.until(EC.element_to_be_clickable((By.ID, input_component_id)))
        InputUtils.setValueUsingComponent(input_component, value)

        xpath = f'.//ul[@id="{aria_controls}"]/li[./div[normalize-space(text())="{value}"]][1]'
        component = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        component.click()
