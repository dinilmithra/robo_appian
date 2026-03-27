from playwright.sync_api import Page

from robo_appian.utils.ComponentUtils import ComponentUtils


class LinkUtils:
    @staticmethod
    def find(page: Page, label: str):
        label_literal = ComponentUtils.xpath_literal(label)
        xpath = (
            ".//a[normalize-space(translate(., '\u00a0', ' '))="
            f'{label_literal} and not(ancestor::*[@aria-hidden="true"])'
            ' and not(ancestor-or-self::*[contains(@class, "---hidden")])]'
        )
        return ComponentUtils.waitForComponentToBeVisibleByXpath(page, xpath)

    @staticmethod
    def click(page: Page, label: str):
        component = LinkUtils.find(page, label)
        ComponentUtils.click(page, component)
        return component
