"""Cart page (`/cart.html`)."""

import re
from decimal import Decimal

from pages.base_page import BasePage
from pages.money import parse_price


class CartPage(BasePage):
    URL = "/cart.html"

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
    def checkout_button(self):
        return self.page.get_by_test_id("checkout")

    @property
    def continue_shopping_button(self):
        return self.page.get_by_test_id("continue-shopping")

    def remove_item_at(self, index: int):
        self.cart_items.nth(index).get_by_role("button", name="Remove").click()

    def open_item_at(self, index: int):
        # Same accessible-name ambiguity as InventoryPage.open_item_at.
        self.cart_items.nth(index).get_by_test_id(re.compile(r"title-link$")).click()

    def checkout(self):
        self.checkout_button.click()

    def continue_shopping(self):
        self.continue_shopping_button.click()
