"""
Checkout flow test suite.

Covers the full happy-path purchase journey end-to-end, price/tax/total
math validation, and required-field errors during checkout -- the kind
of business-logic assertion (not just "did the page load") that
distinguishes a strong QA portfolio piece.
"""
import allure
import pytest

from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from utils.test_data_factory import TestDataFactory


@allure.feature("Checkout")
class TestCheckout:

    @allure.story("Happy path purchase")
    @pytest.mark.smoke
    @pytest.mark.ui
    def test_complete_purchase_end_to_end(
        self,
        logged_in_page: InventoryPage,
        cart_page: CartPage,
        checkout_page: CheckoutPage,
    ):
        logged_in_page.add_item_to_cart_by_name("Sauce Labs Backpack")
        logged_in_page.add_item_to_cart_by_name("Sauce Labs Bike Light")
        logged_in_page.go_to_cart()

        cart_page.checkout()

        info = TestDataFactory.random_checkout_info()
        checkout_page.fill_information(**info)

        assert checkout_page.get_item_count_in_overview() == 2

        checkout_page.finish()

        assert checkout_page.is_order_complete()
        assert "thank you" in checkout_page.get_complete_message().lower()

    @allure.story("Order total math")
    @pytest.mark.regression
    @pytest.mark.ui
    def test_total_equals_subtotal_plus_tax(
        self,
        logged_in_page: InventoryPage,
        cart_page: CartPage,
        checkout_page: CheckoutPage,
    ):
        logged_in_page.add_item_to_cart_by_name("Sauce Labs Backpack")
        logged_in_page.go_to_cart()
        cart_page.checkout()

        info = TestDataFactory.random_checkout_info()
        checkout_page.fill_information(**info)

        subtotal = checkout_page.get_subtotal()
        tax = checkout_page.get_tax()
        total = checkout_page.get_total()

        assert round(subtotal + tax, 2) == round(total, 2)

    @allure.story("Required field validation")
    @pytest.mark.regression
    @pytest.mark.negative
    @pytest.mark.ui
    @pytest.mark.parametrize(
        "first_name,last_name,postal_code,expected_fragment",
        [
            ("", "Doe", "12345", "first name is required"),
            ("John", "", "12345", "last name is required"),
            ("John", "Doe", "", "postal code is required"),
        ],
        ids=["missing-first-name", "missing-last-name", "missing-postal-code"],
    )
    def test_checkout_requires_all_fields(
        self,
        logged_in_page: InventoryPage,
        cart_page: CartPage,
        checkout_page: CheckoutPage,
        first_name,
        last_name,
        postal_code,
        expected_fragment,
    ):
        logged_in_page.add_item_to_cart_by_name("Sauce Labs Backpack")
        logged_in_page.go_to_cart()
        cart_page.checkout()

        checkout_page.fill_information(first_name, last_name, postal_code)

        assert expected_fragment in checkout_page.get_error_message().lower()

    @allure.story("Back to products")
    @pytest.mark.regression
    @pytest.mark.ui
    def test_back_to_products_after_purchase(
        self,
        logged_in_page: InventoryPage,
        cart_page: CartPage,
        checkout_page: CheckoutPage,
    ):
        logged_in_page.add_item_to_cart_by_name("Sauce Labs Backpack")
        logged_in_page.go_to_cart()
        cart_page.checkout()

        info = TestDataFactory.random_checkout_info()
        checkout_page.fill_information(**info)
        checkout_page.finish()

        checkout_page.back_to_products()
        assert logged_in_page.is_loaded()
