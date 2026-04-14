import os
from pathlib import Path

import pytest

from robo_appian.utils.RoboHelper import RoboHelper


def _load_env_file() -> None:
    env_path = Path(__file__).resolve().parents[1] / ".env"
    if not env_path.exists():
        return

    for line in env_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue

        key, value = stripped.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


_load_env_file()


def _is_headless_enabled() -> bool:
    value = os.getenv("HEAD_LESS", "Y").strip().upper()
    if value in {"1", "Y", "YES", "TRUE"}:
        return True
    if value in {"0", "N", "NO", "FALSE"}:
        return False

    raise ValueError("HEAD_LESS must be Y/N, YES/NO, TRUE/FALSE, 1/0, or left unset.")


@pytest.fixture(scope="session")
def browser():
    """Session-scoped Playwright browser.
    Configure via env vars:
      - BROWSER: chromium (default), firefox, or webkit.
      - HEAD_LESS: Y/YES/TRUE/1 enables headless; N/NO/FALSE/0 disables it; leave unset for the default.
    """
    playwright_module = pytest.importorskip("playwright.sync_api")
    browser_name = os.getenv("BROWSER", "chromium").lower()
    headless = _is_headless_enabled()

    with playwright_module.sync_playwright() as playwright:
        if browser_name == "firefox":
            browser_type = playwright.firefox
        elif browser_name == "webkit":
            browser_type = playwright.webkit
        else:
            browser_type = playwright.chromium

        if headless:
            browser_instance = browser_type.launch(headless=True)
        else:
            browser_instance = browser_type.launch(
                headless=False,
                args=["--start-maximized"],
            )
        yield browser_instance
        browser_instance.close()


@pytest.fixture()
def page(browser):
    """Function-scoped Playwright page aligned with library usage (page-first)."""
    wait_time_seconds = int(os.getenv("WAIT_TIME", "15"))
    timeout = wait_time_seconds * 1000
    headless = _is_headless_enabled()

    context_options = {}
    if not headless:
        context_options["no_viewport"] = True
    else:
        context_options["viewport"] = {"width": 1920, "height": 1080}

    context = browser.new_context(**context_options)
    pg = context.new_page()
    pg.set_default_timeout(timeout)

    try:
        RoboHelper.sso_accept(pg)
    except ValueError:
        context.close()
        pytest.skip("APP_URL not set; skipping e2e test.")

    yield pg
    context.close()
