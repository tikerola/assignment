"""Inventory / product list page (`/inventory.html`)."""

import re
from decimal import Decimal

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from pages.base_page import BasePage
from pages.money import parse_price


class InventoryItem:
    """One product card, scoped from InventoryPage.items."""

    def __init__(self, card):
        self._card = card

    @property
    def name(self):
        return self._card.get_by_test_id("inventory-item-name")

    @property
    def price(self):
        return self._card.get_by_test_id("inventory-item-price")

    @property
    def price_value(self) -> Decimal:
        """Item price as a decimal, e.g. "$29.99" -> Decimal("29.99")."""
        return parse_price(self.price.inner_text())

    @property
    def image(self):
        # Each product's image data-test is itself product-specific, so fall back to the CSS
        # class here.
        return self._card.locator(".inventory_item_img img")

    @property
    def add_to_cart_button(self):
        return self._card.get_by_role("button", name="Add to cart")

    def wait_for_image_loaded(self, timeout: float | None = None):
        """Waits until the image has actually rendered real pixel content, not just a src
        attribute (a broken/404 image reports a non-empty src too)."""
        try:
            self.image.page.wait_for_function(
                "(img) => img.complete && img.naturalWidth > 0",
                arg=self.image.element_handle(),
                timeout=timeout,
            )
        except PlaywrightTimeoutError as e:
            raise AssertionError(
                f"Image never loaded for product '{self.name.inner_text()}'"
            ) from e


class InventoryPage(BasePage):
    URL = "/inventory.html"

    @property
    def sort_dropdown(self):
        return self.page.get_by_test_id("product-sort-container")

    @property
    def item_cards(self):
        return self.page.get_by_test_id("inventory-item")

    @property
    def items(self) -> list[InventoryItem]:
        return [InventoryItem(self.item_cards.nth(i)) for i in range(self.item_cards.count())]

    @property
    def item_names(self):
        return self.page.get_by_test_id("inventory-item-name")

    @property
    def item_prices(self):
        return self.page.get_by_test_id("inventory-item-price")

    @property
    def item_price_values(self) -> list[Decimal]:
        """Item prices as decimals, e.g. "$29.99" -> Decimal("29.99")."""
        return [parse_price(p) for p in self.item_prices.all_inner_texts()]

    def add_items_at(self, indexes: list[int]) -> list[InventoryItem]:
        """Adds each indexed item to the cart, returning them in the same order for the
        caller to read back name/price before navigating away from this page."""
        selected = [self.items[i] for i in indexes]
        for item in selected:
            item.add_to_cart_button.click()
        return selected

    def remove_item_at(self, index: int):
        self.item_cards.nth(index).get_by_role("button", name="Remove").click()

    def open_item_at(self, index: int):
        # Suffix match avoids ambiguity with the image link, which shares the same accessible name.
        self.item_cards.nth(index).get_by_test_id(re.compile(r"title-link$")).click()

    def sort_by(self, value: str):
        """value: one of 'az', 'za', 'lohi', 'hilo' (the select element's option values)."""
        self.sort_dropdown.select_option(value)
