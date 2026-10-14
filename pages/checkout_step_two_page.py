"""Checkout step two / overview page (`/checkout-step-two.html`)."""

from decimal import Decimal

from pages.base_page import BasePage
from pages.components.inventory_row_list import InventoryRowList
from pages.money import parse_price


class CheckoutStepTwoPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self._rows = InventoryRowList(page)

    @property
    def cart_items(self):
        return self._rows.cards

    @property
    def item_names(self):
        return self._rows.names

    @property
    def item_price_values(self) -> list[Decimal]:
        return self._rows.price_values

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
