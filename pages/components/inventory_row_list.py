"""Shared read-only view over a page's repeating inventory-item rows: the same
`inventory-item` / `inventory-item-name` / `inventory-item-price` component SauceDemo
renders on the inventory, cart, and checkout-overview pages."""

from decimal import Decimal

from pages.money import parse_price


class InventoryRowList:
    def __init__(self, page):
        self._page = page

    @property
    def cards(self):
        return self._page.get_by_test_id("inventory-item")

    @property
    def names(self):
        return self._page.get_by_test_id("inventory-item-name")

    @property
    def price_values(self) -> list[Decimal]:
        """Item prices as decimals, e.g. "$29.99" -> Decimal("29.99")."""
        return [parse_price(p)
                for p in self._page.get_by_test_id("inventory-item-price").all_inner_texts()]
