"""Checkout complete page (`/checkout-complete.html`)."""

from pages.base_page import BasePage


class CheckoutCompletePage(BasePage):
    @property
    def header(self):
        return self.page.get_by_test_id("complete-header")

    @property
    def complete_text(self):
        return self.page.get_by_test_id("complete-text")
