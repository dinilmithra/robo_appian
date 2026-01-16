import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait


@pytest.fixture(scope="session")
def driver():
    """Session-scoped WebDriver using Selenium Manager (Selenium >= 4.6).
    Configure via env vars:
      - BROWSER: chrome (default). Extend as needed.
      - HEADLESS: "1" (default) to run headless; set "0" for headed.
    """
    browser = os.getenv("BROWSER", "chrome").lower()
    headless = os.getenv("HEADLESS", "1") == "1"

    if browser == "chrome":
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        drv = webdriver.Chrome(options=options)
    else:
        # Fallback to Chrome if an unsupported browser is requested
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        drv = webdriver.Chrome(options=options)

    yield drv
    try:
        drv.quit()
    except Exception:
        pass


@pytest.fixture()
def wait(driver):
    """Function-scoped WebDriverWait aligned with library usage (wait-first)."""
    timeout = int(os.getenv("SELENIUM_WAIT_TIMEOUT", "15"))
    return WebDriverWait(driver, timeout)


@pytest.fixture()
def app_url():
    """Application base URL from APP_URL; skips test if not provided."""
    url = os.getenv("APP_URL")
    if not url:
        pytest.skip("APP_URL not set; skipping e2e test.")
    return url
