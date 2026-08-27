"""Checkout complete page (`/checkout-complete.html`)."""

from pages.base_page import BasePage


class CheckoutCompletePage(BasePage):
    @property
    def header(self):
        return self.page.get_by_test_id("complete-header")

    @property
    def complete_text(self):
        return self.page.get_by_test_id("complete-text")

    @property
    def back_home_button(self):
        return self.page.get_by_test_id("back-to-products")

    @property
    def generate_pdf_button(self):
        return self.page.get_by_test_id("generate-pdf-order")

    def back_home(self):
        self.back_home_button.click()
