try:
    import tomllib
except ImportError:  # pragma: no cover - Python < 3.11
    import tomli as tomllib

import time
from datetime import date, timedelta
from pathlib import Path
from typing import Any, Union

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError, expect

from .AppianUtils import AppianUtils

Page = Any
Locator = Any


class ComponentUtils:

    @staticmethod
    def xpath_literal(value: str) -> str:
        """Convert a string into an XPath-safe literal expression.

        Handles both single and double quotes by using XPath concat() when needed.

        Args:
            value: The string value to convert to an XPath literal.

        Returns:
            str: XPath-safe literal expression (quoted string or concat function call).

        Examples:
            >>> ComponentUtils.xpath_literal('test')
            '"test"'
            >>> ComponentUtils.xpath_literal('test"value')
            "'test\"value'"
            >>> ComponentUtils.xpath_literal('test\'value"')
            'concat("test", "'", "value", "\"")'  # Simplified representation
        """
        if '"' not in value:
            return f'"{value}"'
        if "'" not in value:
            return f'\'{value}\''

        parts = value.split('"')
        literals: list[str] = []
        for index, part in enumerate(parts):
            if part:
                literals.append(f'"{part}"')
            if index < len(parts) - 1:
                literals.append("'\"'")
        return f'concat({", ".join(literals)})'

    @staticmethod
    def xpath_text_with_normalized_nbsp(text_expr: str = ".") -> str:
        """Build XPath text expression with NBSP normalized to regular spaces."""
        return f'translate({text_expr}, \'\u00a0\', \' \')'

    @staticmethod
    def xpath_trim_equals(text_expr: str, expected: str) -> str:
        """Build XPath predicate that trims only outer spaces (not inner spaces)."""
        expected_literal = ComponentUtils.xpath_literal(expected.strip())
        normalized_expr = ComponentUtils.xpath_text_with_normalized_nbsp(text_expr)
        return (
            f'contains({normalized_expr}, {expected_literal})'
            f' and string-length(normalize-space(substring-before({normalized_expr}, {expected_literal})))=0'
            f' and string-length(normalize-space(substring-after({normalized_expr}, {expected_literal})))=0'
        )

    @staticmethod
    def xpath_visible_predicate() -> str:
        """Build XPath predicate that excludes aria/class hidden nodes."""
        return (
            'not(ancestor-or-self::*[@aria-hidden="true"])'
            ' and not(ancestor-or-self::*[contains(@class, "---hidden")])'
        )

    @staticmethod
    def validate_id(element_id: str) -> str:
        """Validate and normalize an element ID for lookups.

        Args:
            element_id: The element ID to validate.

        Returns:
            str: The validated, stripped element ID.

        Raises:
            ValueError: If element_id is None, not a string, or empty/whitespace-only.
        """
        if element_id is None:
            raise ValueError("element_id cannot be None")
        if isinstance(element_id, str):
            stripped = element_id.strip()
            if not stripped:
                raise ValueError("element_id cannot be empty or whitespace-only")
            return stripped
        raise ValueError(
            f'element_id must be a string, got {type(element_id).__name__}'
        )

    @staticmethod
    def validate_text_input(text: str, field_name: str = "text") -> str:
        """Validate and normalize a text input value.

        Args:
            text: The text value to validate.
            field_name: Descriptive field name for error messages.

        Returns:
            str: The validated text with NBSP normalized and outer whitespace trimmed.

        Raises:
            ValueError: If text is None, not a string, or empty/whitespace-only.
        """
        if text is None:
            raise ValueError(f"{field_name} cannot be None")
        if not isinstance(text, str):
            raise ValueError(
                f"{field_name} must be a string, got {type(text).__name__}"
            )

        normalized_text = text.replace("\u00A0", " ").strip()
        if not normalized_text:
            raise ValueError(f"{field_name} cannot be empty or whitespace-only")
        return normalized_text

    @staticmethod
    def validate_label_text(label: str) -> str:
        """Validate and normalize label text for component lookups."""
        return ComponentUtils.validate_text_input(label, "label")

    @staticmethod
    def _as_locator(page: Page, component_or_xpath: Union[Locator, str]) -> Locator:
        if isinstance(component_or_xpath, str):
            return page.locator(f'xpath={component_or_xpath}').first
        return component_or_xpath

    @staticmethod
    def retry_until(
        func,
        timeout=10,
        wait_interval=0.5,
        raise_on_timeout=False,
        timeout_result=None,
        *args,
        **kwargs,
    ):
        """Retry a function until it returns a truthy value or timeout is reached.

        Args:
            func: Callable to retry.
            timeout: Maximum time to retry in seconds. Default: 10.
            wait_interval: Time to wait between retries in seconds. Default: 0.5.
            raise_on_timeout: If True, raise the last exception on timeout. Default: False.
            timeout_result: Value to return if timeout is reached. Default: None.
            *args: Positional arguments to pass to func.
            **kwargs: Keyword arguments to pass to func.

        Returns:
            The return value from func when it succeeds, or timeout_result if timeout is reached.

        Raises:
            TimeoutError: If raise_on_timeout is True and timeout is reached.
            Exception: Any exception from func (not TimeoutError).
        """
        end_time = time.time() + float(timeout)
        last_exc = None
        while time.time() < end_time:
            try:
                result = func(*args, **kwargs)
                if result:
                    return result
            except (TimeoutError, PlaywrightTimeoutError) as exc:
                last_exc = exc
            except Exception:
                raise
            time.sleep(wait_interval)

        if raise_on_timeout:
            if last_exc is not None:
                raise last_exc
            raise TimeoutError(f'Operation did not succeed within {timeout} seconds')

        return timeout_result

    @staticmethod
    def upload_file(page: Page, file_path: str, selector: str = "input[type='file']"):
        """Upload a file using a file input element.

        Args:
            page: Playwright Page object.
            file_path: Path to the file to upload.
            selector: CSS selector for the file input element. Default: "input[type='file']".
        """
        page.locator(selector).first.set_input_files(file_path)

    @staticmethod
    def get_version():
        """Get the version of the robo_appian package from pyproject.toml.

        Returns:
            str: Version string (e.g., "0.0.2"). Returns "0.0.0" if unable to read.
        """
        try:
            toml_path = Path(__file__).parents[2] / "pyproject.toml"
            with open(toml_path, "rb") as handle:
                data = tomllib.load(handle)
                return data.get("tool", {}).get("poetry", {}).get("version", "0.0.0")
        except Exception:
            return "0.0.0"

    @staticmethod
    def today():
        """Get today's date formatted as MM/DD/YYYY.

        Returns:
            str: Today's date in MM/DD/YYYY format.
        """
        return date.today().strftime("%m/%d/%Y")

    @staticmethod
    def yesterday():
        """Get yesterday's date formatted as MM/DD/YYYY.

        Returns:
            str: Yesterday's date in MM/DD/YYYY format.
        """
        return (date.today() - timedelta(days=1)).strftime("%m/%d/%Y")

    @staticmethod
    def findChildComponentByXpath(
        page: Page, component: Union[Locator, str], xpath: str
    ) -> Locator:
        """Find a child component using a relative XPath within a parent component.

        Args:
            page: Playwright Page object.
            component: Parent component (Locator or XPath string).
            xpath: Relative XPath expression to find the child.

        Returns:
            Locator: The child element locator.

        Raises:
            TimeoutError: If child element is not found or not visible.
        """
        parent = ComponentUtils._as_locator(page, component)
        child = parent.locator(f'xpath={xpath}').first
        expect(child).to_be_visible()
        return child

    @staticmethod
    def findComponentById(page: Page, id: str):
        """Find a visible component by its ID attribute.

        Args:
            page: Playwright Page object.
            id: The ID attribute value.

        Returns:
            Locator: The element locator.

        Raises:
            TimeoutError: If element with ID is not found or not visible.
        """
        locator = page.locator(f'xpath=//*[@id="{id}"]').first
        expect(locator).to_be_visible()
        return locator

    @staticmethod
    def checkComponentExistsByXpath(page: Page, xpath: str):
        """Check if a component exists and is visible using XPath.

        Args:
            page: Playwright Page object.
            xpath: XPath expression to locate the element.

        Returns:
            bool: True if element exists and is visible, False otherwise.
        """
        locator = page.locator(f'xpath={xpath}')
        if locator.count() == 0:
            return False
        return locator.first.is_visible()

    @staticmethod
    def checkComponentExistsById(page: Page, id: str):
        """Check if a component with the given ID exists and is visible.

        Args:
            page: Playwright Page object.
            id: The ID attribute value.

        Returns:
            bool: True if element exists and is visible, False otherwise.
        """
        locator = page.locator(f'xpath=//*[@id="{id}"]')
        if locator.count() == 0:
            return False
        return locator.first.is_visible()

    @staticmethod
    def tab(page: Page):
        """Press the Tab keyboard key.

        Args:
            page: Playwright Page object.
        """
        page.keyboard.press("Tab")

    @staticmethod
    def findComponentsByXPath(page: Page, xpath: str):
        """Find all visible and enabled components using XPath.

        Args:
            page: Playwright Page object.
            xpath: XPath expression to locate elements.

        Returns:
            list[Locator]: List of visible and enabled component locators.

        Raises:
            ValueError: If no valid components are found.
        """
        locators = page.locator(f'xpath={xpath}')
        if locators.count() == 0:
            raise ValueError(f'No components found for XPath: {xpath}')

        valid_components: list[Locator] = []
        for idx in range(locators.count()):
            component = locators.nth(idx)
            try:
                if component.is_visible() and component.is_enabled():
                    valid_components.append(component)
            except Exception:
                continue

        if valid_components:
            return valid_components

        raise ValueError(f'No valid components found for XPath: {xpath}')

    @staticmethod
    def findComponentByXPath(page: Page, xpath: str):
        """Find a component using XPath (attached state, not necessarily visible).

        Args:
            page: Playwright Page object.
            xpath: XPath expression to locate the element.

        Returns:
            Locator: The component element locator.
        """
        locator = page.locator(f'xpath={xpath}').first
        locator.wait_for(state="attached")
        return locator

    @staticmethod
    def findComponentUsingXpathAndClick(page: Page, xpath: str):
        """Find a component using XPath and click it.

        Args:
            page: Playwright Page object.
            xpath: XPath expression to locate the element.

        Raises:
            TimeoutError: If element is not found or not visible.
        """
        component = ComponentUtils.waitForComponentToBeVisibleByXpath(page, xpath)
        ComponentUtils.click(page, component)

    @staticmethod
    def click(page: Page, component: Union[Locator, str]):
        """Click a component with safe scrolling behavior.

        Args:
            page: Playwright Page object.
            component: Component locator or XPath string to click.
        """
        locator = ComponentUtils._as_locator(page, component)
        locator.scroll_into_view_if_needed()
        locator.click()

    @staticmethod
    def waitForElementToBeVisibleById(page: Page, id: str):
        """Wait for an element to become visible by ID.

        Args:
            page: Playwright Page object.
            id: The ID attribute value.

        Returns:
            Locator: The element locator once visible.

        Raises:
            TimeoutError: If element does not become visible within timeout.
        """
        locator = page.locator(f'xpath=//*[@id="{id}"]').first
        expect(locator).to_be_visible()
        return locator

    @staticmethod
    def waitForElementNotToBeVisibleById(page: Page, id: str):
        """Wait for an element to become hidden by ID.

        Args:
            page: Playwright Page object.
            id: The ID attribute value.

        Returns:
            True: Once element is hidden.

        Raises:
            TimeoutError: If element does not become hidden within timeout.
        """
        locator = page.locator(f'xpath=//*[@id="{id}"]').first
        locator.wait_for(state="hidden")
        return True

    @staticmethod
    def waitForAppianActionCompleted(page: Page):
        """Wait for Appian progress and loading indicators to clear.

        Args:
            page: Playwright Page object.
        """
        page.wait_for_selector("#appian-nprogress", state="detached")
        page.wait_for_selector(
            ":is(svg[data-owl-icon-name='fa-circle-o-notch'], button.Button---is_loading)",
            state="detached",
        )

    @staticmethod
    def waitForElementToBeVisibleByText(page: Page, text: str):
        """Wait for an element to become visible by exact text match."""
        return AppianUtils.waitForVisibleElementByText(page, text)

    @staticmethod
    def waitForElementNotToBeVisibleByText(page: Page, text: str):
        """Wait for an element to become hidden by exact text match.

        Args:
            page: Playwright Page object.
            text: Exact text to match (NBSP will be normalized).

        Returns:
            True: Once element is hidden.

        Raises:
            TimeoutError: If element does not become hidden within timeout.
        """
        text_predicate = ComponentUtils.xpath_trim_equals(".", text)
        child_text_predicate = ComponentUtils.xpath_trim_equals(".", text)
        xpath = (
            f'//*[{text_predicate} '
            f'and not(*[{child_text_predicate}]) '
            "and not(ancestor-or-self::*[contains(@class, '---hidden')])]"
        )
        return ComponentUtils.waitForComponentNotToBeVisibleByXpath(page, xpath)

    @staticmethod
    def waitForComponentToBeClickableByXpath(
        page: Page, component: Union[Locator, str]
    ):
        """Wait for a component to become visible and clickable by XPath.

        Args:
            page: Playwright Page object.
            component: Component locator or XPath string.

        Returns:
            Locator: The component element locator once visible.
        """
        locator = ComponentUtils._as_locator(page, component)
        expect(locator).to_be_visible()
        return locator

    @staticmethod
    def waitForComponentToBeVisibleByXpath(page: Page, xpath: str):
        """Wait for a component to become visible using XPath.

        Args:
            page: Playwright Page object.
            xpath: XPath expression to locate the element.

        Returns:
            Locator: The element locator once visible.

        Raises:
            TimeoutError: If element does not become visible within timeout.
        """
        locator = page.locator(f'xpath={xpath}').first
        expect(locator).to_be_visible()
        return locator

    @staticmethod
    def waitForComponentToBeInVisible(page: Page, component: Locator):
        """Wait for a component to become hidden.

        Args:
            page: Playwright Page object.
            component: Component locator to wait for.

        Returns:
            True: Once component is hidden.

        Raises:
            TimeoutError: If component does not become hidden within timeout.
        """
        component.wait_for(state="hidden")
        return True

    @staticmethod
    def waitForComponentNotToBeVisibleByXpath(page: Page, xpath: str):
        """Wait for a component to become hidden using XPath.

        Args:
            page: Playwright Page object.
            xpath: XPath expression to locate the element.

        Returns:
            True: Once element is hidden.

        Raises:
            TimeoutError: If element does not become hidden within timeout.
        """
        locator = page.locator(f'xpath={xpath}').first
        locator.wait_for(state="hidden")
        return True
