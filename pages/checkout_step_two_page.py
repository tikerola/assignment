"""Checkout step two / overview page (`/checkout-step-two.html`)."""

import re
from decimal import Decimal

from pages.base_page import BasePage

_PRICE_RE = re.compile(r"\$(\d+\.\d{2})")


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
        return [Decimal(p.replace("$", ""))
                for p in self.page.get_by_test_id("inventory-item-price").all_inner_texts()]

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
    def subtotal_value(self) -> Decimal:
        return Decimal(_PRICE_RE.search(self.subtotal_label.inner_text()).group(1))

    @property
    def tax_value(self) -> Decimal:
        return Decimal(_PRICE_RE.search(self.tax_label.inner_text()).group(1))

    @property
    def total_value(self) -> Decimal:
        return Decimal(_PRICE_RE.search(self.total_label.inner_text()).group(1))

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
