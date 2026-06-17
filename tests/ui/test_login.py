"""
Login test suite.

Covers the happy path plus SauceDemo's documented negative scenarios:
locked-out user, invalid credentials, and required-field validation.
These are the highest-value tests in any portfolio because they show
both positive and negative testing discipline.
"""
import allure
import pytest

from config.settings import settings
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


@allure.feature("Authentication")
class TestLogin:

    @allure.story("Successful login")
    @pytest.mark.smoke
    @pytest.mark.ui
    def test_standard_user_can_log_in(self, login_page: LoginPage, page):
        login_page.load()
        login_page.login(settings.STANDARD_USER, settings.PASSWORD)

        inventory = InventoryPage(page)
        assert inventory.is_loaded(), "Expected to land on the Products page after login"

    @allure.story("Locked out user")
    @pytest.mark.regression
    @pytest.mark.negative
    @pytest.mark.ui
    def test_locked_out_user_sees_error(self, login_page: LoginPage):
        login_page.load()
        login_page.login(settings.LOCKED_USER, settings.PASSWORD)

        assert login_page.is_error_displayed()
        assert "locked out" in login_page.get_error_message().lower()

    @allure.story("Invalid credentials")
    @pytest.mark.regression
    @pytest.mark.negative
    @pytest.mark.ui
    @pytest.mark.parametrize(
        "username,password",
        [
            ("invalid_user", "secret_sauce"),
            ("standard_user", "wrong_password"),
            ("", "secret_sauce"),
        ],
        ids=["unknown-username", "wrong-password", "blank-username"],
    )
    def test_invalid_login_combinations(self, login_page: LoginPage, username, password):
        login_page.load()
        login_page.login(username, password)

        assert login_page.is_error_displayed()

    @allure.story("Required field validation")
    @pytest.mark.regression
    @pytest.mark.negative
    @pytest.mark.ui
    def test_blank_password_shows_error(self, login_page: LoginPage):
        login_page.load()
        login_page.login(settings.STANDARD_USER, "")

        assert login_page.is_error_displayed()
        assert "password" in login_page.get_error_message().lower()

    @allure.story("Error dismissal")
    @pytest.mark.regression
    @pytest.mark.ui
    def test_error_message_can_be_dismissed(self, login_page: LoginPage):
        login_page.load()
        login_page.login("bad_user", "bad_pass")
        assert login_page.is_error_displayed()

        login_page.dismiss_error()
        assert not login_page.is_error_displayed()

    @allure.story("Performance glitch user")
    @pytest.mark.regression
    @pytest.mark.ui
    def test_performance_glitch_user_eventually_logs_in(self, login_page: LoginPage, page):
        # This user is intentionally slow; verifies our waits/timeouts
        # are resilient rather than flaky under latency.
        login_page.load()
        login_page.login(settings.PERFORMANCE_USER, settings.PASSWORD)

        inventory = InventoryPage(page)
        assert inventory.is_loaded()
