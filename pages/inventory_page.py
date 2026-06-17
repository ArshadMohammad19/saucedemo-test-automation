"""Page object for the products/inventory page."""
from playwright.sync_api import Page

from pages.base_page import BasePage


class InventoryPage(BasePage):
    PAGE_TITLE = ".title"
    INVENTORY_ITEM = ".inventory_item"
    ITEM_NAME = ".inventory_item_name"
    ITEM_PRICE = ".inventory_item_price"
    ADD_TO_CART_BUTTON_TEMPLATE = "button[data-test='add-to-cart-{slug}']"
    CART_BADGE = ".shopping_cart_badge"
    CART_LINK = ".shopping_cart_link"
    SORT_DROPDOWN = ".product_sort_container"
    MENU_BUTTON = "#react-burger-menu-btn"
    LOGOUT_LINK = "#logout_sidebar_link"

    def __init__(self, page: Page):
        super().__init__(page)

    def is_loaded(self) -> bool:
        return self.is_visible(self.PAGE_TITLE) and self.get_text(self.PAGE_TITLE) == "Products"

    def get_item_count(self) -> int:
        return self.page.locator(self.INVENTORY_ITEM).count()

    def get_all_item_names(self) -> list[str]:
        return self.page.locator(self.ITEM_NAME).all_inner_texts()

    def get_all_item_prices(self) -> list[float]:
        raw = self.page.locator(self.ITEM_PRICE).all_inner_texts()
        return [float(p.replace("$", "")) for p in raw]

    def add_item_to_cart_by_name(self, item_name: str) -> None:
        slug = item_name.lower().replace(" ", "-").replace(".", "").replace("(", "").replace(")", "")
        item = self.page.locator(self.INVENTORY_ITEM).filter(has_text=item_name)
        item.get_by_role("button", name="Add to cart").click()

    def get_cart_badge_count(self) -> int:
        if self.is_visible(self.CART_BADGE):
            return int(self.get_text(self.CART_BADGE))
        return 0

    def go_to_cart(self) -> None:
        self.click(self.CART_LINK)

    def sort_by(self, option_value: str) -> None:
        self.page.locator(self.SORT_DROPDOWN).select_option(option_value)

    def logout(self) -> None:
        self.click(self.MENU_BUTTON)
        self.click(self.LOGOUT_LINK)
