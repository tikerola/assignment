import pytest
from playwright.sync_api import expect

from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage

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
