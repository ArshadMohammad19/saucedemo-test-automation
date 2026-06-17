"""
Root conftest.py.

Provides:
- Browser/context configuration driven by config/settings.py
- Page object fixtures (login_page, inventory_page, etc.)
- A `logged_in_page` fixture for tests that don't care about the login
  flow itself and just need to start from the inventory page
- An API client fixture
- A pytest hook that attaches a screenshot to Allure (and saves one to
  disk) whenever a UI test fails, plus trace files for debugging
"""
import os
from pathlib import Path

import pytest
import allure
from playwright.sync_api import Page

from config.settings import settings
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from utils.api_client import APIClient
from utils.logger import get_logger

logger = get_logger(__name__)

SCREENSHOT_DIR = Path(__file__).resolve().parent / "screenshots"
SCREENSHOT_DIR.mkdir(exist_ok=True)


# ---------------------------------------------------------------------------
# Browser / context configuration
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    return {
        **browser_type_launch_args,
        "headless": settings.HEADLESS,
        "slow_mo": settings.SLOW_MO,
    }


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {
            "width": settings.VIEWPORT_WIDTH,
            "height": settings.VIEWPORT_HEIGHT,
        },
        "ignore_https_errors": True,
    }


@pytest.fixture(autouse=True)
def _set_default_timeout(page: Page):
    page.set_default_timeout(settings.DEFAULT_TIMEOUT)
    page.set_default_navigation_timeout(settings.NAVIGATION_TIMEOUT)
    yield


# ---------------------------------------------------------------------------
# Page object fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def login_page(page: Page) -> LoginPage:
    return LoginPage(page)


@pytest.fixture
def inventory_page(page: Page) -> InventoryPage:
    return InventoryPage(page)


@pytest.fixture
def cart_page(page: Page) -> CartPage:
    return CartPage(page)


@pytest.fixture
def checkout_page(page: Page) -> CheckoutPage:
    return CheckoutPage(page)


@pytest.fixture
def logged_in_page(page: Page) -> InventoryPage:
    """Starts the test already authenticated as the standard user and
    sitting on the inventory page, for tests that don't need to exercise
    the login flow itself."""
    login = LoginPage(page)
    login.load()
    login.login(settings.STANDARD_USER, settings.PASSWORD)
    inventory = InventoryPage(page)
    inventory.expect_visible(InventoryPage.PAGE_TITLE)
    return inventory


# ---------------------------------------------------------------------------
# API fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def api_client() -> APIClient:
    return APIClient()


# ---------------------------------------------------------------------------
# Failure capture: screenshot + Allure attachment on UI test failure
# ---------------------------------------------------------------------------

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page: Page | None = item.funcargs.get("page")
        if page is not None:
            screenshot_path = SCREENSHOT_DIR / f"{item.name}.png"
            try:
                page.screenshot(path=str(screenshot_path), full_page=True)
                allure.attach.file(
                    str(screenshot_path),
                    name="failure_screenshot",
                    attachment_type=allure.attachment_type.PNG,
                )
                logger.error("Test '%s' failed. Screenshot saved: %s", item.name, screenshot_path)
            except Exception as exc:  # pragma: no cover - best-effort capture
                logger.warning("Could not capture failure screenshot: %s", exc)
