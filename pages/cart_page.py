"""Page object for the shopping cart page."""
from pages.base_page import BasePage


class CartPage(BasePage):
    CART_ITEM = ".cart_item"
    ITEM_NAME = ".inventory_item_name"
    REMOVE_BUTTON_TEMPLATE = "button[data-test='remove-{slug}']"
    CHECKOUT_BUTTON = "#checkout"
    CONTINUE_SHOPPING_BUTTON = "#continue-shopping"

    def get_item_count(self) -> int:
        return self.page.locator(self.CART_ITEM).count()

    def get_item_names(self) -> list[str]:
        return self.page.locator(self.ITEM_NAME).all_inner_texts()

    def remove_item_by_name(self, item_name: str) -> None:
        item = self.page.locator(self.CART_ITEM).filter(has_text=item_name)
        item.get_by_role("button", name="Remove").click()

    def checkout(self) -> None:
        self.click(self.CHECKOUT_BUTTON)

    def continue_shopping(self) -> None:
        self.click(self.CONTINUE_SHOPPING_BUTTON)
