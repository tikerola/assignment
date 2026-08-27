"""Checkout step two / overview page (`/checkout-step-two.html`)."""

from pages.base_page import BasePage


class CheckoutStepTwoPage(BasePage):
    @property
    def cart_items(self):
        return self.page.get_by_test_id("inventory-item")

    @property
    def payment_info(self):
        return self.page.get_by_test_id("payment-info-value")

    @property
    def shipping_info(self):
        return self.page.get_by_test_id("shipping-info-value")

    @property
    def subtotal_label(self):
        return self.page.get_by_test_id("subtotal-label")

    @property
    def tax_label(self):
        return self.page.get_by_test_id("tax-label")

    @property
    def total_label(self):
        return self.page.get_by_test_id("total-label")

    @property
    def cancel_button(self):
        return self.page.get_by_test_id("cancel")

    @property
    def finish_button(self):
        return self.page.get_by_test_id("finish")

    def finish(self):
        self.finish_button.click()

    def cancel(self):
        self.cancel_button.click()
