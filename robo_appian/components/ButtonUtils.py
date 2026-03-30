from typing import Any

from robo_appian.utils.ComponentUtils import ComponentUtils

Page = Any


class ButtonUtils:
    @staticmethod
    def _findByPartialLabelText(page: Page, label: str):
        label_literal = ComponentUtils.xpath_literal(label.strip())
        button_text = ComponentUtils.xpath_text_with_normalized_nbsp(".")
        xpath = (
            f"//button[contains({button_text}, "
            f"{label_literal})"
            ' and not(ancestor::*[@aria-hidden="true"])'
            ' and not(ancestor-or-self::*[contains(@class, "---hidden")])]' 
        )
        return ComponentUtils.waitForComponentToBeVisibleByXpath(page, xpath)

    @staticmethod
    def _findByLabelText(page: Page, label: str):
        label_predicate = ComponentUtils.xpath_trim_equals(".", label)
        xpath = (
            f"//button[./span[{label_predicate}]"
            ' and not(ancestor::*[@aria-hidden="true"])'
            ' and not(ancestor-or-self::*[contains(@class, "---hidden")])]'
        )
        return ComponentUtils.waitForComponentToBeVisibleByXpath(page, xpath)

    @staticmethod
    def clickByPartialLabelText(page: Page, label: str):
        """Click a button by partial label text match.

        Args:
            page: Playwright Page object.
            label: Partial text to match in the button label.

        Raises:
            TimeoutError: If button is not found or not visible.
        """
        component = ButtonUtils._findByPartialLabelText(page, label)
        ComponentUtils.click(page, component)

    @staticmethod
    def clickByLabelText(page: Page, label: str):
        """Click a button by exact label text match.

        Args:
            page: Playwright Page object.
            label: Exact text to match in the button label.

        Raises:
            TimeoutError: If button is not found or not visible.
        """
        component = ButtonUtils._findByLabelText(page, label)
        ComponentUtils.click(page, component)

    @staticmethod
    def clickById(page: Page, id: str):
        """Click an element by ID.

        Args:
            page: Playwright Page object.
            id: The ID attribute of the element.

        Raises:
            TimeoutError: If element is not found or not visible.
        """
        xpath = f"//*[@id={ComponentUtils.xpath_literal(id)}]"
        component = ComponentUtils.waitForComponentToBeVisibleByXpath(page, xpath)
        ComponentUtils.click(page, component)

    @staticmethod
    def isButtonExistsByLabelText(page: Page, label: str):
        """Check if a button exists by exact label text match.

        Args:
            page: Playwright Page object.
            label: Exact text to match in the button label.

        Returns:
            bool: True if button exists and is visible, False otherwise.
        """
        label_predicate = ComponentUtils.xpath_trim_equals(".", label)
        xpath = (
            f"//button[./span[{label_predicate}]"
            ' and not(ancestor::*[@aria-hidden="true"])'
            ' and not(ancestor-or-self::*[contains(@class, "---hidden")])]'
        )
        return ComponentUtils.checkComponentExistsByXpath(page, xpath)

    @staticmethod
    def isButtonExistsByPartialLabelText(page: Page, label: str):
        """Check if a button exists by partial label text match.

        Args:
            page: Playwright Page object.
            label: Partial text to match in the button label.

        Returns:
            bool: True if button exists and is visible, False otherwise.
        """
        label_literal = ComponentUtils.xpath_literal(label.strip())
        button_text = ComponentUtils.xpath_text_with_normalized_nbsp(".")
        xpath = (
            f"//button[contains({button_text}, "
            f"{label_literal})"
            ' and not(ancestor::*[@aria-hidden="true"])'
            ' and not(ancestor-or-self::*[contains(@class, "---hidden")])]' 
        )
        return ComponentUtils.checkComponentExistsByXpath(page, xpath)

    @staticmethod
    def isButtonExistsByPartialLabelTextAfterLoad(page: Page, label: str):
        """Check if a button exists after waiting with retry logic.

        Args:
            page: Playwright Page object.
            label: Partial text to match in the button label.

        Returns:
            bool: True if button appears within the retry window, False otherwise.
        """
        return bool(
            ComponentUtils.retry_until(
                lambda: ButtonUtils.isButtonExistsByPartialLabelText(page, label),
                timeout_result=False,
            )
        )

    @staticmethod
    def waitForButtonToBeVisibleByPartialLabelText(page: Page, label: str):
        """Wait for a button to become visible by partial label text match.

        Args:
            page: Playwright Page object.
            label: Partial text to match in the button label.

        Returns:
            Locator: The button element once visible.

        Raises:
            TimeoutError: If button does not become visible within timeout.
        """
        label_literal = ComponentUtils.xpath_literal(label.strip())
        button_text = ComponentUtils.xpath_text_with_normalized_nbsp(".")
        xpath = (
            f"//button[contains({button_text}, "
            f"{label_literal})"
            ' and not(ancestor::*[@aria-hidden="true"])'
            ' and not(ancestor-or-self::*[contains(@class, "---hidden")])]' 
        )
        return ComponentUtils.waitForComponentToBeVisibleByXpath(page, xpath)
