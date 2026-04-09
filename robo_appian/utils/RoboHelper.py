import os

from playwright.sync_api import Page, expect


class RoboHelper:
    """Helper utilities for Playwright-based test setup flows."""

    @staticmethod
    def sso_accept(page: Page) -> bool:
        """Navigate to APP_URL and accept the FDA SSO security warning when shown."""
        app_url = os.getenv("APP_URL")
        if not app_url:
            raise ValueError("APP_URL cannot be empty")

        page.goto(app_url.strip(), wait_until="domcontentloaded")
        page.wait_for_load_state("networkidle")

        accept_locator = page.locator(
            'a.btn[title="Accept"], a[onclick*="postAccept"], form[action*="SSO.ping"] a:has-text("Accept")'
        ).first

        expect(accept_locator).to_be_visible()
        accept_locator.scroll_into_view_if_needed()
        accept_locator.click(force=True)

        page.wait_for_load_state("domcontentloaded")
        page.wait_for_load_state("networkidle")
        return True
