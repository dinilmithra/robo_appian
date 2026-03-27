try:
    import tomllib
except ImportError:  # pragma: no cover - Python < 3.11
    import tomli as tomllib

import time
from datetime import date, timedelta
from pathlib import Path
from typing import Any, Union

Page = Any
Locator = Any


class ComponentUtils:

    @staticmethod
    def xpath_literal(value: str) -> str:
        if '"' not in value:
            return f'"{value}"'
        if "'" not in value:
            return f"'{value}'"

        parts = value.split('"')
        literals: list[str] = []
        for index, part in enumerate(parts):
            if part:
                literals.append(f'"{part}"')
            if index < len(parts) - 1:
                literals.append("'\"'")
        return f"concat({', '.join(literals)})"

    @staticmethod
    def _as_locator(page: Page, component_or_xpath: Union[Locator, str]) -> Locator:
        if isinstance(component_or_xpath, str):
            return page.locator(f"xpath={component_or_xpath}").first
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
        end_time = time.time() + float(timeout)
        last_exc = None
        while time.time() < end_time:
            try:
                result = func(*args, **kwargs)
                if result:
                    return result
            except Exception as exc:
                last_exc = exc
            time.sleep(wait_interval)

        if raise_on_timeout:
            if last_exc is not None:
                raise last_exc
            raise TimeoutError(f"Operation did not succeed within {timeout} seconds")

        return timeout_result

    @staticmethod
    def upload_file(page: Page, file_path: str, selector: str = "input[type='file']"):
        page.locator(selector).first.set_input_files(file_path)

    @staticmethod
    def get_version():
        try:
            toml_path = Path(__file__).parents[2] / "pyproject.toml"
            with open(toml_path, "rb") as handle:
                data = tomllib.load(handle)
                return data.get("tool", {}).get("poetry", {}).get("version", "0.0.0")
        except Exception:
            return "0.0.0"

    @staticmethod
    def today():
        return date.today().strftime("%m/%d/%Y")

    @staticmethod
    def yesterday():
        return (date.today() - timedelta(days=1)).strftime("%m/%d/%Y")

    @staticmethod
    def findChildComponentByXpath(
        page: Page, component: Union[Locator, str], xpath: str
    ) -> Locator:
        parent = ComponentUtils._as_locator(page, component)
        child = parent.locator(f"xpath={xpath}").first
        child.wait_for(state="visible")
        return child

    @staticmethod
    def findComponentById(page: Page, id: str):
        locator = page.locator(f'xpath=//*[@id="{id}"]').first
        locator.wait_for(state="visible")
        return locator

    @staticmethod
    def checkComponentExistsByXpath(page: Page, xpath: str):
        locator = page.locator(f"xpath={xpath}")
        if locator.count() == 0:
            return False
        return locator.first.is_visible()

    @staticmethod
    def checkComponentExistsById(page: Page, id: str):
        locator = page.locator(f'xpath=//*[@id="{id}"]')
        if locator.count() == 0:
            return False
        return locator.first.is_visible()

    @staticmethod
    def tab(page: Page):
        page.keyboard.press("Tab")

    @staticmethod
    def findComponentsByXPath(page: Page, xpath: str):
        locators = page.locator(f"xpath={xpath}")
        if locators.count() == 0:
            raise ValueError(f"No components found for XPath: {xpath}")

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

        raise ValueError(f"No valid components found for XPath: {xpath}")

    @staticmethod
    def findComponentByXPath(page: Page, xpath: str):
        locator = page.locator(f"xpath={xpath}").first
        locator.wait_for(state="attached")
        return locator

    @staticmethod
    def findComponentUsingXpathAndClick(page: Page, xpath: str):
        component = ComponentUtils.waitForComponentToBeVisibleByXpath(page, xpath)
        ComponentUtils.click(page, component)

    @staticmethod
    def click(page: Page, component: Union[Locator, str]):
        locator = ComponentUtils._as_locator(page, component)
        locator.scroll_into_view_if_needed()
        locator.click()

    @staticmethod
    def waitForElementToBeVisibleById(page: Page, id: str):
        locator = page.locator(f'xpath=//*[@id="{id}"]').first
        locator.wait_for(state="visible")
        return locator

    @staticmethod
    def waitForElementNotToBeVisibleById(page: Page, id: str):
        locator = page.locator(f'xpath=//*[@id="{id}"]').first
        locator.wait_for(state="hidden")
        return True

    @staticmethod
    def waitForElementToBeVisibleByText(page: Page, text: str):
        xpath = (
            f'//*[normalize-space(translate(., "\u00a0", " "))="{text}" '
            f'and not(*[normalize-space(translate(., "\u00a0", " "))="{text}"]) '
            f'and not(ancestor-or-self::*[contains(@class, "---hidden")])]'
        )
        return ComponentUtils.waitForComponentToBeVisibleByXpath(page, xpath)

    @staticmethod
    def waitForElementNotToBeVisibleByText(page: Page, text: str):
        xpath = (
            f'//*[normalize-space(translate(., "\u00a0", " "))="{text}" '
            f'and not(*[normalize-space(translate(., "\u00a0", " "))="{text}"]) '
            f'and not(ancestor-or-self::*[contains(@class, "---hidden")])]'
        )
        return ComponentUtils.waitForComponentNotToBeVisibleByXpath(page, xpath)

    @staticmethod
    def waitForComponentToBeClickableByXpath(
        page: Page, component: Union[Locator, str]
    ):
        locator = ComponentUtils._as_locator(page, component)
        locator.wait_for(state="visible")
        return locator

    @staticmethod
    def waitForComponentToBeVisibleByXpath(page: Page, xpath: str):
        locator = page.locator(f"xpath={xpath}").first
        locator.wait_for(state="visible")
        return locator

    @staticmethod
    def waitForComponentToBeInVisible(page: Page, component: Locator):
        component.wait_for(state="hidden")
        return True

    @staticmethod
    def waitForComponentNotToBeVisibleByXpath(page: Page, xpath: str):
        locator = page.locator(f"xpath={xpath}").first
        locator.wait_for(state="hidden")
        return True
