"""Shared header/nav/footer chrome present on every authenticated saucedemo.com page."""


class BasePage:
    def __init__(self, page):
        self.page = page

    @property
    def cart_link(self):
        return self.page.get_by_test_id("shopping-cart-link")

    @property
    def cart_badge(self):
        return self.page.get_by_test_id("shopping-cart-badge")

    def open_cart(self):
        self.cart_link.click()

    @property
    def menu_open_button(self):
        # No data-test on these two, unlike everything else -- id is the only stable selector.
        return self.page.locator("#react-burger-menu-btn")

    @property
    def menu_close_button(self):
        return self.page.locator("#react-burger-cross-btn")

    def open_menu(self):
        self.menu_open_button.click()

    def close_menu(self):
        self.menu_close_button.click()

    def go_to_all_items(self):
        self.open_menu()
        self.page.get_by_test_id("inventory-sidebar-link").click()

    def logout(self):
        self.open_menu()
        self.page.get_by_test_id("logout-sidebar-link").click()

    def reset_app_state(self):
        self.open_menu()
        self.page.get_by_test_id("reset-sidebar-link").click()
        self.close_menu()

    @property
    def social_twitter_link(self):
        return self.page.get_by_test_id("social-twitter")

    @property
    def social_facebook_link(self):
        return self.page.get_by_test_id("social-facebook")

    @property
    def social_linkedin_link(self):
        return self.page.get_by_test_id("social-linkedin")
