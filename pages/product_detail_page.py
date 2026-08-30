"""Product detail page (`/inventory-item.html?id=N`)."""

from decimal import Decimal

from pages.base_page import BasePage
from pages.money import parse_price


class ProductDetailPage(BasePage):
    @property
    def item_name(self):
        return self.page.get_by_test_id("inventory-item-name")

    @property
    def item_price(self):
        return self.page.get_by_test_id("inventory-item-price")

    @property
    def item_price_value(self) -> Decimal:
        """Item price as a decimal, e.g. "$29.99" -> Decimal("29.99")."""
        return parse_price(self.item_price.inner_text())

    @property
    def add_to_cart_button(self):
        return self.page.get_by_test_id("add-to-cart")

    @property
    def remove_button(self):
        return self.page.get_by_test_id("remove")

    @property
    def back_to_products_button(self):
        return self.page.get_by_test_id("back-to-products")

    def add_to_cart(self):
        self.add_to_cart_button.click()

    def back_to_products(self):
        self.back_to_products_button.click()
