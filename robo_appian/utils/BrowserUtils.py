from playwright.sync_api import Locator, Page


class BrowserUtils:

    @staticmethod
    def switch_to_tab(page: Page, locator: Locator) -> Page:
        """Click a locator that opens a new tab and return the new page."""
        with page.context.expect_page() as new_page_info:
            locator.click()

        new_page = new_page_info.value
        new_page.wait_for_load_state("domcontentloaded")
        return new_page

    @staticmethod
    def switch_to_next_tab(page: Page) -> Page:
        """Switch to the next open tab relative to the current page."""
        pages = [open_page for open_page in page.context.pages if not open_page.is_closed()]
        current_tab_index = pages.index(page)
        next_tab_index = (current_tab_index + 1) % len(pages)
        target = pages[next_tab_index]
        target.bring_to_front()
        target.wait_for_load_state("networkidle")
        return target

    # @staticmethod
    # def switch_to_Tab(page: Page, tab_number: int):
    #     """Switch to a specific browser tab.

    #     Args:
    #         page: Current Playwright Page object.
    #         tab_number: Zero-based index of the tab to switch to.

    #     Returns:
    #         Page: The target page/tab object.

    #     Raises:
    #         IndexError: If tab_number is out of range.
    #     """
    #     pages = page.context.pages
    #     target = pages[tab_number]
    #     target.bring_to_front()
    #     return target

    # @staticmethod
    # def switch_to_next_tab(page: Page):
        # """Switch to the next browser tab in circular order.

        # Args:
        #     page: Current Playwright Page object.

        # Returns:
        #     Page: The next page/tab object.
        # """
        # pages = page.context.pages
        # current_tab_index = pages.index(page)
        # next_tab_index = (current_tab_index + 1) % len(pages)
        # return BrowserUtils.switch_to_Tab(page, next_tab_index)

    @staticmethod
    def close_current_tab_and_switch_back(page: Page):
        """Close the current tab and switch back to the previous tab.

        Args:
            page: Current Playwright Page object.

        Returns:
            Page: The previous page/tab object.

        Raises:
            ValueError: If attempting to close the only open tab.
        """
        context = page.context
        pages = [open_page for open_page in context.pages if not open_page.is_closed()]
        if len(pages) <= 1:
            raise ValueError("Cannot switch back after closing the only open tab.")

        current_tab_index = pages.index(page)
        page.close()
        pages = [open_page for open_page in context.pages if not open_page.is_closed()]
        original_tab_index = (current_tab_index - 1) % len(pages)
        target = pages[original_tab_index]
        target.bring_to_front()
        return target
