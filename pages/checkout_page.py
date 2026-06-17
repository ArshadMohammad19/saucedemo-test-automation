"""
Page object for the checkout flow.

SauceDemo's checkout spans three URLs/steps: information entry,
overview/confirmation, and the final success/complete screen. Modeling
all three in one class keeps the flow cohesive while still exposing
step-specific methods.
"""
from pages.base_page import BasePage


class CheckoutPage(BasePage):
    # Step 1: information
    FIRST_NAME_INPUT = "#first-name"
    LAST_NAME_INPUT = "#last-name"
    POSTAL_CODE_INPUT = "#postal-code"
    CONTINUE_BUTTON = "#continue"
    ERROR_MESSAGE = "[data-test='error']"

    # Step 2: overview
    FINISH_BUTTON = "#finish"
    SUMMARY_SUBTOTAL = ".summary_subtotal_label"
    SUMMARY_TAX = ".summary_tax_label"
    SUMMARY_TOTAL = ".summary_total_label"
    CART_ITEM = ".cart_item"

    # Step 3: complete
    COMPLETE_HEADER = ".complete-header"
    BACK_HOME_BUTTON = "#back-to-products"

    def fill_information(self, first_name: str, last_name: str, postal_code: str) -> None:
        self.fill(self.FIRST_NAME_INPUT, first_name)
        self.fill(self.LAST_NAME_INPUT, last_name)
        self.fill(self.POSTAL_CODE_INPUT, postal_code)
        self.click(self.CONTINUE_BUTTON)

    def get_error_message(self) -> str:
        return self.get_text(self.ERROR_MESSAGE)

    def get_item_count_in_overview(self) -> int:
        return self.page.locator(self.CART_ITEM).count()

    def get_subtotal(self) -> float:
        text = self.get_text(self.SUMMARY_SUBTOTAL)
        return float(text.split("$")[-1])

    def get_tax(self) -> float:
        text = self.get_text(self.SUMMARY_TAX)
        return float(text.split("$")[-1])

    def get_total(self) -> float:
        text = self.get_text(self.SUMMARY_TOTAL)
        return float(text.split("$")[-1])

    def finish(self) -> None:
        self.click(self.FINISH_BUTTON)

    def is_order_complete(self) -> bool:
        return self.is_visible(self.COMPLETE_HEADER)

    def get_complete_message(self) -> str:
        return self.get_text(self.COMPLETE_HEADER)

    def back_to_products(self) -> None:
        self.click(self.BACK_HOME_BUTTON)
