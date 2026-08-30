"""Shared header chrome present on every authenticated saucedemo.com page."""


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
