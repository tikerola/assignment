"""Cart page (`/cart.html`)."""

from decimal import Decimal

from pages.base_page import BasePage
from pages.components.inventory_row_list import InventoryRowList


class CartPage(BasePage):
    URL = "/cart.html"

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
    def checkout_button(self):
        return self.page.get_by_test_id("checkout")

    def remove_item_at(self, index: int):
        self.cart_items.nth(index).get_by_role("button", name="Remove").click()

    def checkout(self):
        self.checkout_button.click()
