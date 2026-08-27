"""Product detail page (`/inventory-item.html?id=N`)."""

from pages.base_page import BasePage


class ProductDetailPage(BasePage):
    @property
    def item_name(self):
        return self.page.get_by_test_id("inventory-item-name")

    @property
    def item_desc(self):
        return self.page.get_by_test_id("inventory-item-desc")

    @property
    def item_price(self):
        return self.page.get_by_test_id("inventory-item-price")

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

    def remove_from_cart(self):
        self.remove_button.click()

    def back_to_products(self):
        self.back_to_products_button.click()
