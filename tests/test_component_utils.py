"""Unit tests for ComponentUtils."""

import time
import pytest
from datetime import date, timedelta
from unittest.mock import MagicMock, patch, call
from selenium.common.exceptions import NoSuchElementException

from robo_appian.utils.ComponentUtils import ComponentUtils


def make_wait(element=None):
    wait = MagicMock()
    wait._driver = MagicMock()
    if element is not None:
        wait.until.return_value = element
    return wait


class TestRetryUntil:
    def test_returns_truthy_immediately(self):
        func = MagicMock(return_value="ok")
        result = ComponentUtils.retry_until(func, timeout=1)
        assert result == "ok"

    @patch("robo_appian.utils.ComponentUtils.time")
    def test_retries_until_truthy(self, mock_time):
        # Make time.time advance only when called explicitly
        mock_time.time.side_effect = [0, 0, 0, 0, 100]  # triggers timeout guard
        mock_time.sleep = MagicMock()
        func = MagicMock(side_effect=[None, None, "result"])
        result = ComponentUtils.retry_until(func, timeout=10)
        assert result == "result"

    @patch("robo_appian.utils.ComponentUtils.time")
    def test_returns_false_on_timeout(self, mock_time):
        mock_time.time.side_effect = [0, 100]
        mock_time.sleep = MagicMock()
        func = MagicMock(return_value=None)
        result = ComponentUtils.retry_until(func, timeout=1)
        assert result is False

    @patch("robo_appian.utils.ComponentUtils.time")
    def test_raise_on_timeout_with_last_exception(self, mock_time):
        mock_time.time.side_effect = [0, 0, 100]
        mock_time.sleep = MagicMock()
        func = MagicMock(side_effect=ValueError("fail"))
        with pytest.raises(ValueError, match="fail"):
            ComponentUtils.retry_until(func, timeout=1, raise_on_timeout=True)

    @patch("robo_appian.utils.ComponentUtils.time")
    def test_raise_on_timeout_no_exception_raises_timeout_error(self, mock_time):
        mock_time.time.side_effect = [0, 100]
        mock_time.sleep = MagicMock()
        func = MagicMock(return_value=None)
        with pytest.raises(TimeoutError):
            ComponentUtils.retry_until(func, timeout=1, raise_on_timeout=True)


class TestToday:
    def test_today_format(self):
        result = ComponentUtils.today()
        today = date.today()
        assert result == today.strftime("%m/%d/%Y")
        assert len(result) == 10
        parts = result.split("/")
        assert len(parts) == 3


class TestYesterday:
    def test_yesterday_format(self):
        result = ComponentUtils.yesterday()
        yesterday = date.today() - timedelta(days=1)
        assert result == yesterday.strftime("%m/%d/%Y")
        assert len(result) == 10


class TestGetVersion:
    def test_returns_string(self):
        version = ComponentUtils.get_version()
        assert isinstance(version, str)
        assert len(version) > 0

    def test_returns_fallback_on_missing_file(self):
        with patch("builtins.open", side_effect=FileNotFoundError):
            version = ComponentUtils.get_version()
        assert version == "0.0.0"


class TestCheckComponentExistsById:
    def test_returns_true_when_found(self):
        driver = MagicMock()
        driver.find_element.return_value = MagicMock()
        assert ComponentUtils.checkComponentExistsById(driver, "my-id") is True

    def test_returns_false_when_not_found(self):
        driver = MagicMock()
        driver.find_element.side_effect = NoSuchElementException()
        assert ComponentUtils.checkComponentExistsById(driver, "missing-id") is False


class TestCheckComponentExistsByXpath:
    def test_returns_true_when_found(self):
        wait = make_wait()
        with patch.object(
            ComponentUtils, "waitForComponentToBeVisibleByXpath", return_value=MagicMock()
        ):
            assert ComponentUtils.checkComponentExistsByXpath(wait, "//div") is True

    def test_returns_false_when_exception(self):
        wait = make_wait()
        with patch.object(
            ComponentUtils,
            "waitForComponentToBeVisibleByXpath",
            side_effect=NoSuchElementException(),
        ):
            assert ComponentUtils.checkComponentExistsByXpath(wait, "//div") is False


class TestFindComponentById:
    def test_finds_component_by_id(self):
        mock_el = MagicMock()
        wait = make_wait(mock_el)
        result = ComponentUtils.findComponentById(wait, "some-id")
        assert result == mock_el


class TestFindComponentByXPath:
    def test_returns_element(self):
        mock_el = MagicMock()
        wait = make_wait()
        wait._driver.find_element.return_value = mock_el
        result = ComponentUtils.findComponentByXPath(wait, "//span")
        assert result == mock_el

    def test_raises_no_such_element(self):
        wait = make_wait()
        wait._driver.find_element.side_effect = NoSuchElementException()
        with pytest.raises(NoSuchElementException):
            ComponentUtils.findComponentByXPath(wait, "//span")


class TestWaitForComponentToBeVisibleByXpath:
    def test_returns_element(self):
        mock_el = MagicMock()
        wait = make_wait(mock_el)
        result = ComponentUtils.waitForComponentToBeVisibleByXpath(wait, "//div")
        assert result == mock_el


class TestFindChildComponentByXpath:
    def test_finds_child(self):
        child_el = MagicMock()
        parent_el = MagicMock()
        parent_el.find_element.return_value = child_el
        wait = MagicMock()
        wait.until.side_effect = lambda fn: fn(None)
        result = ComponentUtils.findChildComponentByXpath(wait, parent_el, ".//span")
        assert result == child_el


class TestClick:
    def test_click_calls_action_chains(self):
        mock_el = MagicMock()
        wait = make_wait()
        with patch("robo_appian.utils.ComponentUtils.ActionChains") as MockAC:
            mock_actions = MagicMock()
            MockAC.return_value = mock_actions
            mock_actions.move_to_element.return_value = mock_actions
            mock_actions.click.return_value = mock_actions
            ComponentUtils.click(wait, mock_el)
            MockAC.assert_called_once_with(wait._driver)
            mock_actions.move_to_element.assert_called_once_with(mock_el)
            mock_actions.click.assert_called_once()
            mock_actions.perform.assert_called_once()


class TestFindComponentsByXPath:
    def test_returns_valid_components(self):
        mock_el = MagicMock()
        mock_el.is_displayed.return_value = True
        mock_el.is_enabled.return_value = True
        wait = make_wait()
        wait._driver.find_elements.return_value = [mock_el]
        result = ComponentUtils.findComponentsByXPath(wait, "//div")
        assert mock_el in result

    def test_raises_when_no_valid_components(self):
        mock_el = MagicMock()
        mock_el.is_displayed.return_value = False
        wait = make_wait()
        wait._driver.find_elements.return_value = [mock_el]
        with pytest.raises(Exception, match="No valid components found"):
            ComponentUtils.findComponentsByXPath(wait, "//div")


class TestWaitForElementVisibility:
    def test_wait_for_visible_by_id(self):
        mock_el = MagicMock()
        wait = make_wait(mock_el)
        result = ComponentUtils.waitForElementToBeVisibleById(wait, "my-id")
        assert result == mock_el

    def test_wait_for_not_visible_by_id(self):
        wait = make_wait(True)
        result = ComponentUtils.waitForElementNotToBeVisibleById(wait, "my-id")
        assert result is True

    def test_wait_for_visible_by_text(self):
        mock_el = MagicMock()
        wait = make_wait(mock_el)
        result = ComponentUtils.waitForElementToBeVisibleByText(wait, "Hello")
        assert result == mock_el

    def test_wait_for_not_visible_by_text(self):
        wait = make_wait(True)
        result = ComponentUtils.waitForElementNotToBeVisibleByText(wait, "Hello")
        assert result is True

    def test_wait_for_not_visible_by_xpath(self):
        wait = make_wait(True)
        result = ComponentUtils.waitForComponentNotToBeVisibleByXpath(wait, "//div")
        assert result is True


class TestTab:
    def test_tab_sends_tab_key(self):
        wait = make_wait()
        with patch("robo_appian.utils.ComponentUtils.ActionChains") as MockAC:
            mock_actions = MagicMock()
            MockAC.return_value = mock_actions
            mock_actions.send_keys.return_value = mock_actions
            ComponentUtils.tab(wait)
            mock_actions.perform.assert_called_once()
