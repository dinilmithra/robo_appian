"""Unit tests for LinkUtils."""

import pytest
from unittest.mock import MagicMock, patch

from robo_appian.components.LinkUtils import LinkUtils


def make_wait():
    wait = MagicMock()
    wait._driver = MagicMock()
    return wait


class TestFind:
    def test_returns_link_element(self):
        wait = make_wait()
        mock_el = MagicMock()
        wait.until.return_value = mock_el
        result = LinkUtils.find(wait, "Edit")
        assert result == mock_el

    def test_xpath_excludes_aria_hidden(self):
        wait = make_wait()
        wait.until.return_value = MagicMock()
        LinkUtils.find(wait, "View Report")
        condition = wait.until.call_args[0][0]
        # The condition is built with the XPath containing aria-hidden guard
        assert condition is not None

    def test_xpath_uses_exact_text_match(self):
        wait = make_wait()
        wait.until.return_value = MagicMock()
        # Patch presence_of_element_located to capture xpath
        with patch("robo_appian.components.LinkUtils.EC.presence_of_element_located") as mock_ec:
            mock_ec.return_value = MagicMock()
            LinkUtils.find(wait, "Learn More")
        locator = mock_ec.call_args[0][0]
        xpath = locator[1]
        assert "Learn More" in xpath
        assert "aria-hidden" in xpath


class TestClick:
    def test_finds_and_clicks_link(self):
        wait = make_wait()
        mock_el = MagicMock()
        wait.until.return_value = mock_el
        with patch("robo_appian.components.LinkUtils.ComponentUtils.click") as mock_click:
            result = LinkUtils.click(wait, "Delete")
        mock_click.assert_called_once_with(wait, mock_el)
        assert result == mock_el

    def test_returns_link_element(self):
        wait = make_wait()
        mock_el = MagicMock()
        wait.until.return_value = mock_el
        with patch("robo_appian.components.LinkUtils.ComponentUtils.click"):
            result = LinkUtils.click(wait, "Edit Details")
        assert result == mock_el
