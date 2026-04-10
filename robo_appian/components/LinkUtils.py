from playwright.sync_api import Page


class LinkUtils:

    @staticmethod
    def click(page: Page, label: str):
        """
        Clicks a link by label text if it and its ancestors are not aria-hidden.
        """
        # 1. Locate the link by its user-visible role and text.
        # This is the "Playwright Style" start point.
        links = page.get_by_role("link", name=label, exact=True)

        # 2. Create an exclusion filter for hidden ancestors.
        # :not([aria-hidden='true'])   -> The element itself isn't hidden.
        # :not([aria-hidden='true'] *) -> The element is not inside a hidden parent.
        not_hidden_selector = ":not([aria-hidden='true']):not([aria-hidden='true'] *)"

        # 3. Chain the locators.
        # .and_() intersects the 'link' locator with the 'not hidden' locator.
        # .filter(visible=True) ensures it's actually on the screen.
        locator = (
            links.and_(page.locator(not_hidden_selector)).filter(visible=True).first
        )

        # 4. Perform the click on the first valid match.
        # .first handles cases where Appian might have temporary DOM duplicates.
        locator.click()
        return locator
