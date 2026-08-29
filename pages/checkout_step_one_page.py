"""Checkout step one / info page (`/checkout-step-one.html`)."""

from pages.base_page import BasePage


class CheckoutStepOnePage(BasePage):
    URL = "/checkout-step-one.html"

    @property
    def first_name_input(self):
        return self.page.get_by_test_id("firstName")

    @property
    def last_name_input(self):
        return self.page.get_by_test_id("lastName")

    @property
    def postal_code_input(self):
        return self.page.get_by_test_id("postalCode")

    @property
    def error_message(self):
        return self.page.get_by_test_id("error")

    @property
    def cancel_button(self):
        return self.page.get_by_test_id("cancel")

    @property
    def continue_button(self):
        return self.page.get_by_test_id("continue")

    def fill_info(self, first_name: str, last_name: str, postal_code: str):
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.postal_code_input.fill(postal_code)

    def continue_to_overview(self):
        self.continue_button.click()

    def cancel(self):
        self.cancel_button.click()
