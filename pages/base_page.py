"""
Base page object. All page classes inherit from this to share common,
low-level helpers (navigation, waiting, generic element interaction) so
individual page classes can stay focused on page-specific behavior.
"""
from playwright.sync_api import Page, expect

from config.settings import settings


class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.base_url = settings.BASE_URL

    def goto(self, path: str = "/") -> None:
        url = self.base_url if path == "/" else f"{self.base_url}{path}"
        self.page.goto(url, timeout=settings.NAVIGATION_TIMEOUT)

    def title(self) -> str:
        return self.page.title()

    def current_url(self) -> str:
        return self.page.url

    def wait_for_url_contains(self, fragment: str, timeout: int | None = None) -> None:
        self.page.wait_for_url(f"**/*{fragment}*", timeout=timeout or settings.NAVIGATION_TIMEOUT)

    def is_visible(self, selector: str) -> bool:
        return self.page.locator(selector).is_visible()

    def get_text(self, selector: str) -> str:
        return self.page.locator(selector).inner_text()

    def click(self, selector: str) -> None:
        self.page.locator(selector).click()

    def fill(self, selector: str, value: str) -> None:
        locator = self.page.locator(selector)
        locator.fill("")
        locator.fill(value)

    def expect_visible(self, selector: str) -> None:
        expect(self.page.locator(selector)).to_be_visible()

    def expect_text(self, selector: str, text: str) -> None:
        expect(self.page.locator(selector)).to_have_text(text)

    def take_screenshot(self, path: str) -> None:
        self.page.screenshot(path=path, full_page=True)
