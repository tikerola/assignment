"""Checkout step two / overview page (`/checkout-step-two.html`)."""

from decimal import Decimal

from pages.base_page import BasePage
from pages.money import parse_price


class CheckoutStepTwoPage(BasePage):
    @property
    def cart_items(self):
        return self.page.get_by_test_id("inventory-item")

    @property
    def item_names(self):
        return self.page.get_by_test_id("inventory-item-name")

    @property
    def item_price_values(self) -> list[Decimal]:
        """Item prices as decimals, e.g. "$29.99" -> Decimal("29.99")."""
        return [parse_price(p)
                for p in self.page.get_by_test_id("inventory-item-price").all_inner_texts()]

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
    def subtotal_value(self) -> Decimal:
        return parse_price(self.subtotal_label.inner_text())

    @property
    def tax_value(self) -> Decimal:
        return parse_price(self.tax_label.inner_text())

    @property
    def total_value(self) -> Decimal:
        return parse_price(self.total_label.inner_text())

    @property
    def finish_button(self):
        return self.page.get_by_test_id("finish")

    def finish(self):
        self.finish_button.click()
