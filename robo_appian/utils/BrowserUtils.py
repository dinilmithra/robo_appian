from selenium.webdriver.support.ui import WebDriverWait


class BrowserUtils:
    @staticmethod
    def switch_to_Tab(wait: WebDriverWait, tab_number):
        """
        Switches to the specified browser tab.

        :param wait: WebDriverWait instance
        :param tab_number: The index of the tab to switch to
        :return: None
        Example usage:
            BrowserUtils.switch_to_Tab(wait, 1)
        """

        # Switch to the specified browser tab
        handler = wait._driver.window_handles[tab_number]
        wait._driver.switch_to.window(handler)

    @staticmethod
    def switch_to_next_tab(wait: WebDriverWait):
        """
        Switches to the next browser tab.

        :param wait: WebDriverWait instance
        :return: None
        Example usage:
            BrowserUtils.switch_to_next_tab(wait)
        """
        current_tab_index = wait._driver.window_handles.index(
            wait._driver.current_window_handle
        )
        next_tab_index = (current_tab_index + 1) % len(wait._driver.window_handles)
        BrowserUtils.switch_to_Tab(wait, next_tab_index)

    @staticmethod
    def close_current_tab_and_switch_back(wait: WebDriverWait):
        """
        Closes the current browser tab and switches back to the original tab.

        :param wait: WebDriverWait instance
        :return: None
        Example usage:
            BrowserUtils.close_current_tab_and_switch_back(wait)
        """
        current_tab_index = wait._driver.window_handles.index(
            wait._driver.current_window_handle
        )
        wait._driver.close()
        original_tab_index = (current_tab_index - 1) % len(wait._driver.window_handles)
        BrowserUtils.switch_to_Tab(wait, original_tab_index)
