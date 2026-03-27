from playwright.sync_api import Page

from robo_appian.utils.ComponentUtils import ComponentUtils


class TabUtils:
    @staticmethod
    def findTabByLabelText(page: Page, label: str):
        label_literal = ComponentUtils.xpath_literal(label)
        xpath = (
            "//div[@role=\"link\"][.//p[normalize-space(translate(., '\u00a0', ' '))="
            f"{label_literal}]]"
        )
        return ComponentUtils.waitForComponentToBeVisibleByXpath(page, xpath)

    @staticmethod
    def selectTabByLabelText(page: Page, label: str):
        component = TabUtils.findTabByLabelText(page, label)
        ComponentUtils.click(page, component)

    @staticmethod
    def checkTabSelectedByLabelText(page: Page, label: str):
        component = TabUtils.findTabByLabelText(page, label)
        selected_attr = component.get_attribute("aria-selected")
        selected_indicator = component.locator(
            'xpath=.//span[normalize-space(.)="Selected Tab."]'
        )
        return selected_attr == "true" or selected_indicator.count() > 0
