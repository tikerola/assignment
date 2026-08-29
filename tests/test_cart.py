import pytest
from playwright.sync_api import expect

from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage
from pages.product_detail_page import ProductDetailPage

pytestmark = pytest.mark.regression


def test_cart_state_integrity_across_add_and_remove(logged_in_page):
    inventory = InventoryPage(logged_in_page)

    selected_items = inventory.add_items_at([0, 1, 2])
    expected_names = [item.name.inner_text() for item in selected_items]
    expect(inventory.cart_badge).to_have_text(str(len(expected_names)))

    # Remove the middle item directly from the inventory page.
    inventory.remove_item_at(1)
    expected_names.pop(1)
    expect(inventory.cart_badge).to_have_text(str(len(expected_names)))

    inventory.open_cart()
    cart = CartPage(logged_in_page)
    expect(cart.cart_items).to_have_count(len(expected_names))
    assert cart.item_names.all_inner_texts() == expected_names

    # Remove the first remaining item directly from the cart page.
    cart.remove_item_at(0)
    expected_names.pop(0)
    expect(cart.cart_items).to_have_count(len(expected_names))
    assert cart.item_names.all_inner_texts() == expected_names
    expect(cart.cart_badge).to_have_text(str(len(expected_names)))


def test_add_to_cart_from_product_detail_page_persists_state(logged_in_page):
    inventory = InventoryPage(logged_in_page)
    inventory.open_item_at(0)

    detail = ProductDetailPage(logged_in_page)
    expected_name = detail.item_name.inner_text()
    expected_price = detail.item_price_value

    detail.add_to_cart()
    expect(detail.remove_button).to_be_visible()
    expect(detail.cart_badge).to_have_text("1")

    # Navigating away and back to the same product preserves the "added" state.
    detail.back_to_products()
    inventory.open_item_at(0)
    expect(detail.remove_button).to_be_visible()

    detail.open_cart()
    cart = CartPage(logged_in_page)
    expect(cart.cart_items).to_have_count(1)
    assert cart.item_names.all_inner_texts() == [expected_name]
    assert cart.item_price_values == [expected_price]
