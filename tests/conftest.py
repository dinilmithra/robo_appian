import os
import pytest


@pytest.fixture(scope="session")
def browser():
    """Session-scoped Playwright browser.
    Configure via env vars:
      - BROWSER: chromium (default), firefox, or webkit.
      - HEADLESS: "1" (default) to run headless; set "0" for headed.
    """
    playwright_module = pytest.importorskip("playwright.sync_api")
    browser_name = os.getenv("BROWSER", "chromium").lower()
    headless = os.getenv("HEADLESS", "1") == "1"

    with playwright_module.sync_playwright() as playwright:
        if browser_name == "firefox":
            browser_type = playwright.firefox
        elif browser_name == "webkit":
            browser_type = playwright.webkit
        else:
            browser_type = playwright.chromium

        browser_instance = browser_type.launch(headless=headless)
        yield browser_instance
        browser_instance.close()


@pytest.fixture()
def page(browser):
    """Function-scoped Playwright page aligned with library usage (page-first)."""
    timeout = int(os.getenv("PLAYWRIGHT_TIMEOUT_MS", "15000"))
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    pg = context.new_page()
    pg.set_default_timeout(timeout)
    yield pg
    context.close()


@pytest.fixture()
def app_url():
    """Application base URL from APP_URL; skips test if not provided."""
    url = os.getenv("APP_URL")
    if not url:
        pytest.skip("APP_URL not set; skipping e2e test.")
    return url
