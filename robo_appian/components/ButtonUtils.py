from typing import Any

from robo_appian.utils.ComponentUtils import ComponentUtils

Page = Any


class ButtonUtils:
    @staticmethod
    def _findByPartialLabelText(page: Page, label: str):
        label_literal = ComponentUtils.xpath_literal(label)
        xpath = (
            "//button[contains(normalize-space(translate(., '\u00a0', ' ')), "
            f"{label_literal})"
            ' and not(ancestor::*[@aria-hidden="true"])'
            ' and not(ancestor-or-self::*[contains(@class, "---hidden")])]' 
        )
        return ComponentUtils.waitForComponentToBeVisibleByXpath(page, xpath)

    @staticmethod
    def _findByLabelText(page: Page, label: str):
        label_literal = ComponentUtils.xpath_literal(label)
        xpath = (
            "//button[./span[normalize-space(translate(., '\u00a0', ' '))="
            f"{label_literal}]]"
        )
        return ComponentUtils.waitForComponentToBeVisibleByXpath(page, xpath)

    @staticmethod
    def clickByPartialLabelText(page: Page, label: str):
        component = ButtonUtils._findByPartialLabelText(page, label)
        ComponentUtils.click(page, component)

    @staticmethod
    def clickByLabelText(page: Page, label: str):
        component = ButtonUtils._findByLabelText(page, label)
        ComponentUtils.click(page, component)

    @staticmethod
    def clickById(page: Page, id: str):
        xpath = f"//*[@id={ComponentUtils.xpath_literal(id)}]"
        component = ComponentUtils.waitForComponentToBeVisibleByXpath(page, xpath)
        ComponentUtils.click(page, component)

    @staticmethod
    def isButtonExistsByLabelText(page: Page, label: str):
        label_literal = ComponentUtils.xpath_literal(label)
        xpath = (
            "//button[./span[normalize-space(translate(., '\u00a0', ' '))="
            f"{label_literal}]]"
        )
        return ComponentUtils.checkComponentExistsByXpath(page, xpath)

    @staticmethod
    def isButtonExistsByPartialLabelText(page: Page, label: str):
        label_literal = ComponentUtils.xpath_literal(label)
        xpath = (
            "//button[contains(normalize-space(translate(., '\u00a0', ' ')), "
            f"{label_literal})"
            ' and not(ancestor::*[@aria-hidden="true"])'
            ' and not(ancestor-or-self::*[contains(@class, "---hidden")])]' 
        )
        return ComponentUtils.checkComponentExistsByXpath(page, xpath)

    @staticmethod
    def isButtonExistsByPartialLabelTextAfterLoad(page: Page, label: str):
        return bool(
            ComponentUtils.retry_until(
                lambda: ButtonUtils.isButtonExistsByPartialLabelText(page, label),
                timeout_result=False,
            )
        )

    @staticmethod
    def waitForButtonToBeVisibleByPartialLabelText(page: Page, label: str):
        label_literal = ComponentUtils.xpath_literal(label)
        xpath = (
            "//button[contains(normalize-space(translate(., '\u00a0', ' ')), "
            f"{label_literal})"
            ' and not(ancestor::*[@aria-hidden="true"])'
            ' and not(ancestor-or-self::*[contains(@class, "---hidden")])]' 
        )
        return ComponentUtils.waitForComponentToBeVisibleByXpath(page, xpath)
