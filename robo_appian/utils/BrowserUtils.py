from selenium.webdriver.support.ui import WebDriverWait


class BrowserUtils:
    """
    Manage browser windows and tabs: switch between tabs, open new windows, and close tabs.

    Use these utilities when your Appian automation spans multiple browser tabs or windows.
    All methods follow the wait-first pattern: pass WebDriverWait as the first argument.

    Examples:
        >>> from robo_appian import BrowserUtils
        >>> BrowserUtils.switch_to_Tab(wait, 1)  # Switch to second tab
        >>> BrowserUtils.switch_to_next_tab(wait)  # Move to next tab
        >>> BrowserUtils.close_current_tab_and_switch_back(wait)  # Close and return
    """

    @staticmethod
    def switch_to_Tab(wait: WebDriverWait, tab_number):
        """
        Switch to a specific browser tab by index.

        Finds the tab by its position in window_handles and switches the driver context to it.

        Args:
            wait: WebDriverWait instance.
            tab_number: Zero-based index of the tab to switch to (0 = first tab, 1 = second, etc.).

        Returns:
            None

        Raises:
            IndexError: If tab_number is out of range for available tabs.

        Examples:
            >>> BrowserUtils.switch_to_Tab(wait, 0)  # First tab
            >>> BrowserUtils.switch_to_Tab(wait, 1)  # Second tab
        """

        # Switch to the specified browser tab
        handler = wait._driver.window_handles[tab_number]
        wait._driver.switch_to.window(handler)

    @staticmethod
    def switch_to_next_tab(wait: WebDriverWait):
        """
        Switch to the next browser tab in sequence.

        Moves to the next tab after the current one. If already on the last tab,
        wraps around to the first tab.

        Args:
            wait: WebDriverWait instance.

        Returns:
            None

        Examples:
            >>> BrowserUtils.switch_to_next_tab(wait)  # Cycles through available tabs
        """
        current_tab_index = wait._driver.window_handles.index(
            wait._driver.current_window_handle
        )
        next_tab_index = (current_tab_index + 1) % len(wait._driver.window_handles)
        BrowserUtils.switch_to_Tab(wait, next_tab_index)

    @staticmethod
    def close_current_tab_and_switch_back(wait: WebDriverWait):
        """
        Close the current browser tab and return to the previous tab.

        Useful when Appian navigation opens a link in a new tab and you need to
        close it after completing an action. Automatically switches back to the
        previous tab index.

        Args:
            wait: WebDriverWait instance.

        Returns:
            None

        Examples:
            >>> # Open a new tab, perform actions, then close it
            >>> BrowserUtils.close_current_tab_and_switch_back(wait)
        """
        current_tab_index = wait._driver.window_handles.index(
            wait._driver.current_window_handle
        )
        wait._driver.close()
        original_tab_index = (current_tab_index - 1) % len(wait._driver.window_handles)
        BrowserUtils.switch_to_Tab(wait, original_tab_index)
