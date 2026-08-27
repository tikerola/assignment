"""Cart page (`/cart.html`)."""

import re

from pages.base_page import BasePage


class CartPage(BasePage):
    @property
    def cart_items(self):
        return self.page.get_by_test_id("inventory-item")

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
