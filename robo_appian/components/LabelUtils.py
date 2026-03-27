from playwright.sync_api import Page

from robo_appian.utils.ComponentUtils import ComponentUtils


class LabelUtils:
    @staticmethod
    def __findByLabelText(page: Page, label: str):
        label_literal = ComponentUtils.xpath_literal(label)
        xpath = (
            "//*[self::label or self::span or self::p or self::a or self::abbr]"
            f"[normalize-space(translate(., '\u00a0', ' '))={label_literal}"
            f" and not(descendant::*[self::label or self::span or self::p or self::a or self::abbr][normalize-space(translate(., '\u00a0', ' '))={label_literal}])"
            ' and not(ancestor::*[@aria-hidden="true"])'
            ' and not(ancestor-or-self::*[contains(@class, "---hidden")])]'
        )
        return ComponentUtils.waitForComponentToBeVisibleByXpath(page, xpath)

    @staticmethod
    def clickByLabelText(page: Page, label: str):
        component = LabelUtils.__findByLabelText(page, label)
        ComponentUtils.click(page, component)

    @staticmethod
    def isLabelExists(page: Page, label: str):
        label_literal = ComponentUtils.xpath_literal(label)
        xpath = (
            "//*[self::label or self::span or self::p or self::a or self::abbr]"
            f"[normalize-space(translate(., '\u00a0', ' '))={label_literal}"
            f" and not(descendant::*[self::label or self::span or self::p or self::a or self::abbr][normalize-space(translate(., '\u00a0', ' '))={label_literal}])"
            ' and not(ancestor::*[@aria-hidden="true"])'
            ' and not(ancestor-or-self::*[contains(@class, "---hidden")])]'
        )
        return ComponentUtils.checkComponentExistsByXpath(page, xpath)
