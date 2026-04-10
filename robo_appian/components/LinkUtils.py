from playwright.sync_api import Page


class LinkUtils:

    @staticmethod
    def click(page: Page, label: str):
        """
        Clicks a visible link with the specified text, 
        ensuring it is not inside an aria-hidden container.
        """
        # The CSS selector logic:
        # 1. :not([aria-hidden="true"]) * -> Look inside elements that are NOT hidden.
        # 2. a:has-text("{label}")        -> Find an 'a' tag that contains the text.
        # 3. :visible                     -> Playwright pseudo-class to ensure it's on screen.
        
        selector = f':not([aria-hidden="true"]) * a:has-text("{label}"):visible'
        
        # In Playwright style, you don't need explicit waits. 
        # .click() automatically waits for the element matching the selector to appear.
        locator = page.locator(selector).first
        locator.click()
        return locator
