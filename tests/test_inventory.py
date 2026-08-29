
import pytest

from pages.inventory_page import InventoryPage

pytestmark = pytest.mark.regression


@pytest.mark.parametrize(
    "sort_value, get_values, reverse",
    [
        ("lohi", lambda inv: inv.item_price_values, False),
        ("hilo", lambda inv: inv.item_price_values, True),
        ("az", lambda inv: inv.item_names.all_inner_texts(), False),
        ("za", lambda inv: inv.item_names.all_inner_texts(), True),
    ],
    ids=["price_low_to_high", "price_high_to_low", "name_a_to_z", "name_z_to_a"],
)
def test_sort_inventory(logged_in_page, sort_value, get_values, reverse):
    inv = InventoryPage(logged_in_page)
    inv.sort_by(sort_value)
    values = get_values(inv)
    assert values == sorted(values, reverse=reverse)


