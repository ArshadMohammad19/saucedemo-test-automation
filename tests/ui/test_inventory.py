"""
Inventory page test suite.

Covers product listing integrity, sorting behavior, and a deliberate
test against the "problem_user" account, which SauceDemo seeds with a
known UI bug (all product images are identical) -- a good example of
testing for a *known defect* rather than assuming the app is always
correct.
"""
import allure
import pytest

from config.settings import settings
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


@allure.feature("Inventory")
class TestInventory:

    @allure.story("Product listing")
    @pytest.mark.smoke
    @pytest.mark.ui
    def test_all_products_are_displayed(self, logged_in_page: InventoryPage):
        assert logged_in_page.get_item_count() == settings.EXPECTED_ITEM_COUNT

        names = logged_in_page.get_all_item_names()
        assert set(names) == set(settings.EXPECTED_ITEMS)

    @allure.story("Sorting")
    @pytest.mark.regression
    @pytest.mark.ui
    def test_sort_by_price_low_to_high(self, logged_in_page: InventoryPage):
        logged_in_page.sort_by("lohi")
        prices = logged_in_page.get_all_item_prices()

        assert prices == sorted(prices)

    @allure.story("Sorting")
    @pytest.mark.regression
    @pytest.mark.ui
    def test_sort_by_price_high_to_low(self, logged_in_page: InventoryPage):
        logged_in_page.sort_by("hilo")
        prices = logged_in_page.get_all_item_prices()

        assert prices == sorted(prices, reverse=True)

    @allure.story("Sorting")
    @pytest.mark.regression
    @pytest.mark.ui
    def test_sort_by_name_a_to_z(self, logged_in_page: InventoryPage):
        logged_in_page.sort_by("az")
        names = logged_in_page.get_all_item_names()

        assert names == sorted(names)

    @allure.story("Sorting")
    @pytest.mark.regression
    @pytest.mark.ui
    def test_sort_by_name_z_to_a(self, logged_in_page: InventoryPage):
        logged_in_page.sort_by("za")
        names = logged_in_page.get_all_item_names()

        assert names == sorted(names, reverse=True)

    @allure.story("Cart badge")
    @pytest.mark.smoke
    @pytest.mark.ui
    def test_cart_badge_updates_on_add(self, logged_in_page: InventoryPage):
        assert logged_in_page.get_cart_badge_count() == 0

        logged_in_page.add_item_to_cart_by_name("Sauce Labs Backpack")
        assert logged_in_page.get_cart_badge_count() == 1

        logged_in_page.add_item_to_cart_by_name("Sauce Labs Bike Light")
        assert logged_in_page.get_cart_badge_count() == 2

    @allure.story("Logout")
    @pytest.mark.regression
    @pytest.mark.ui
    def test_logout_returns_to_login_page(self, logged_in_page: InventoryPage, login_page: LoginPage):
        logged_in_page.logout()
        login_page.expect_visible(LoginPage.LOGIN_BUTTON)
