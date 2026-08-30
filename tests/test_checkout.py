import random
from decimal import ROUND_HALF_UP, Decimal

import pytest
from playwright.sync_api import expect

from pages.cart_page import CartPage
from pages.checkout_complete_page import CheckoutCompletePage
from pages.checkout_step_one_page import CheckoutStepOnePage
from pages.checkout_step_two_page import CheckoutStepTwoPage
from pages.inventory_page import InventoryPage

pytestmark = pytest.mark.regression

# SauceDemo applies an 8% tax rate.
TAX_RATE = Decimal("0.08")


@pytest.mark.smoke
def test_happy_path_full_purchase_with_price_verification(logged_in_page):
    inventory = InventoryPage(logged_in_page)

    # Random 3 of the full catalog, not a fixed [0, 1, 2] -- rotates coverage across every
    # product's image/name/price over repeated runs instead of always exercising the same three.
    item_count = len(inventory.items)
    assert item_count >= 3, f"Expected at least 3 products in the catalog, found {item_count}"
    indexes = random.sample(range(item_count), 3)
    selected_items = inventory.add_items_at(indexes)
    for item in selected_items:
        item.wait_for_image_loaded()
    expected_names = [item.name.inner_text() for item in selected_items]
    expected_prices = [item.price_value for item in selected_items]

    expect(inventory.cart_badge).to_have_text(str(len(selected_items)))

    inventory.open_cart()
    cart = CartPage(logged_in_page)
    expect(cart.cart_items).to_have_count(len(selected_items))
    assert cart.item_names.all_inner_texts() == expected_names
    assert cart.item_price_values == expected_prices

    cart.checkout()
    step_one = CheckoutStepOnePage(logged_in_page)
    step_one.fill_info("Lucky", "Luke", "00100")
    step_one.continue_to_overview()

    step_two = CheckoutStepTwoPage(logged_in_page)
    expect(step_two.cart_items).to_have_count(len(selected_items))
    assert step_two.item_names.all_inner_texts() == expected_names
    assert step_two.item_price_values == expected_prices

    expected_subtotal = sum(expected_prices)
    expected_tax = (expected_subtotal * TAX_RATE).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    assert step_two.subtotal_value == expected_subtotal
    assert step_two.tax_value == expected_tax
    assert step_two.total_value == expected_subtotal + expected_tax

    step_two.finish()

    complete = CheckoutCompletePage(logged_in_page)
    expect(complete.header).to_have_text("Thank you for your order!")
    expect(complete.complete_text).to_be_visible()


@pytest.mark.parametrize(
    "first_name, last_name, postal_code, expected_error",
    [
        ("", "Doe", "12345", "Error: First Name is required"),
        ("John", "", "12345", "Error: Last Name is required"),
        ("John", "Doe", "", "Error: Postal Code is required"),
        ("", "", "", "Error: First Name is required"),
    ],
    ids=["missing_first_name", "missing_last_name", "missing_postal_code", "all_fields_empty"],
)
def test_checkout_requires_customer_information(
    logged_in_page, first_name, last_name, postal_code, expected_error
):
    inventory = InventoryPage(logged_in_page)
    inventory.add_items_at([0])
    inventory.open_cart()

    cart = CartPage(logged_in_page)
    cart.checkout()

    step_one = CheckoutStepOnePage(logged_in_page)
    step_one.fill_info(first_name, last_name, postal_code)
    step_one.continue_to_overview()

    expect(step_one.error_message).to_have_text(expected_error)
    expect(logged_in_page).to_have_url(CheckoutStepOnePage.URL)


@pytest.mark.xfail(
    reason="saucedemo does not block checkout with an empty cart -- documenting this as a known "
    "gap on the assumption that a zero-item order would carry real business impact "
    "(invoicing, fulfillment, reporting) in a production system",
    strict=True,
)
def test_checkout_blocks_empty_cart(logged_in_page):
    inventory = InventoryPage(logged_in_page)
    inventory.open_cart()

    cart = CartPage(logged_in_page)
    expect(cart.cart_items).to_have_count(0)
    cart.checkout()

    expect(logged_in_page).to_have_url(CartPage.URL)
