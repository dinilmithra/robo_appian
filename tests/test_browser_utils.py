"""Unit tests for BrowserUtils."""

import pytest
from unittest.mock import MagicMock, call, patch

from robo_appian.utils.BrowserUtils import BrowserUtils


def make_wait(handles, current_handle):
    wait = MagicMock()
    wait._driver = MagicMock()
    wait._driver.window_handles = handles
    wait._driver.current_window_handle = current_handle
    return wait


class TestSwitchToTab:
    def test_switches_to_first_tab(self):
        handles = ["h0", "h1", "h2"]
        wait = make_wait(handles, "h0")
        BrowserUtils.switch_to_Tab(wait, 0)
        wait._driver.switch_to.window.assert_called_once_with("h0")

    def test_switches_to_second_tab(self):
        handles = ["h0", "h1", "h2"]
        wait = make_wait(handles, "h0")
        BrowserUtils.switch_to_Tab(wait, 1)
        wait._driver.switch_to.window.assert_called_once_with("h1")

    def test_raises_index_error_on_out_of_range(self):
        handles = ["h0"]
        wait = make_wait(handles, "h0")
        with pytest.raises(IndexError):
            BrowserUtils.switch_to_Tab(wait, 5)


class TestSwitchToNextTab:
    def test_switches_to_next_tab(self):
        handles = ["h0", "h1", "h2"]
        wait = make_wait(handles, "h0")
        BrowserUtils.switch_to_next_tab(wait)
        wait._driver.switch_to.window.assert_called_once_with("h1")

    def test_wraps_around_from_last_to_first(self):
        handles = ["h0", "h1", "h2"]
        wait = make_wait(handles, "h2")
        BrowserUtils.switch_to_next_tab(wait)
        wait._driver.switch_to.window.assert_called_once_with("h0")

    def test_single_tab_wraps_to_itself(self):
        handles = ["h0"]
        wait = make_wait(handles, "h0")
        BrowserUtils.switch_to_next_tab(wait)
        wait._driver.switch_to.window.assert_called_once_with("h0")


class TestCloseCurrentTabAndSwitchBack:
    def test_closes_current_tab_and_switches_to_previous(self):
        from unittest.mock import PropertyMock

        wait = MagicMock()
        driver = MagicMock()
        wait._driver = driver
        driver.current_window_handle = "h1"

        # First access → ["h0", "h1"] (before close); subsequent → ["h0"] (after close)
        type(driver).window_handles = PropertyMock(
            side_effect=[["h0", "h1"], ["h0"], ["h0"]]
        )

        BrowserUtils.close_current_tab_and_switch_back(wait)
        driver.close.assert_called_once()
        driver.switch_to.window.assert_called_once_with("h0")

    def test_close_first_tab_wraps_to_last(self):
        from unittest.mock import PropertyMock

        # Current is h0 (index 0). After close only h1 remains → (0-1) % 1 = 0 → switches to h1
        wait = MagicMock()
        driver = MagicMock()
        wait._driver = driver
        driver.current_window_handle = "h0"

        type(driver).window_handles = PropertyMock(
            side_effect=[["h0", "h1"], ["h1"], ["h1"]]
        )

        BrowserUtils.close_current_tab_and_switch_back(wait)
        driver.close.assert_called_once()
        driver.switch_to.window.assert_called_once_with("h1")
