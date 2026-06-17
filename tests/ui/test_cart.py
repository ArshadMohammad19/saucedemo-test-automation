"""Shopping cart test suite: add/remove items, navigate to/from cart."""
import allure
import pytest

from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage


@allure.feature("Cart")
class TestCart:

    @allure.story("Add and view cart")
    @pytest.mark.smoke
    @pytest.mark.ui
    def test_added_items_appear_in_cart(self, logged_in_page: InventoryPage, cart_page: CartPage):
        logged_in_page.add_item_to_cart_by_name("Sauce Labs Backpack")
        logged_in_page.add_item_to_cart_by_name("Sauce Labs Fleece Jacket")
        logged_in_page.go_to_cart()

        assert cart_page.get_item_count() == 2
        assert set(cart_page.get_item_names()) == {
            "Sauce Labs Backpack",
            "Sauce Labs Fleece Jacket",
        }

    @allure.story("Remove from cart")
    @pytest.mark.regression
    @pytest.mark.ui
    def test_remove_item_from_cart(self, logged_in_page: InventoryPage, cart_page: CartPage):
        logged_in_page.add_item_to_cart_by_name("Sauce Labs Backpack")
        logged_in_page.go_to_cart()
        assert cart_page.get_item_count() == 1

        cart_page.remove_item_by_name("Sauce Labs Backpack")
        assert cart_page.get_item_count() == 0

    @allure.story("Continue shopping")
    @pytest.mark.regression
    @pytest.mark.ui
    def test_continue_shopping_returns_to_inventory(
        self, logged_in_page: InventoryPage, cart_page: CartPage
    ):
        logged_in_page.go_to_cart()
        cart_page.continue_shopping()

        assert logged_in_page.is_loaded()

    @allure.story("Empty cart")
    @pytest.mark.regression
    @pytest.mark.ui
    def test_cart_is_empty_by_default(self, logged_in_page: InventoryPage, cart_page: CartPage):
        logged_in_page.go_to_cart()
        assert cart_page.get_item_count() == 0
