import pytest
from logic import _retain_only_items_in_stock

@pytest.mark.parametrize(
    "items, inventory, expected", [
        ([], [], []),
        ([], [{"item_id": 1, "stock": 11}], []),
        ([{"id": 1, "name": "p_1", "price": 10}], [], []),
        ([{"id": 1, "name": "p_1", "price": 10}], [{"item_id": 2, "stock": 11}], []),
        ([{"id": 1, "name": "p_1", "price": 10}], [{"item_id": 1, "stock": 11}], [{"id": 1, "name": "p_1", "price": 10, "stock": 11}]),
        ([{"id": 1, "name": "p_1", "price": 10}, {"id": 2, "name": "p_1", "price": 10}], [{"item_id": 1, "stock": 11}], [{"id": 1, "name": "p_1", "price": 10, "stock": 11}]),
        ([{"id": 1, "name": "p_1", "price": 10}], [{"item_id": 1, "stock": 11}, {"item_id": 2, "stock": 11}], [{"id": 1, "name": "p_1", "price": 10, "stock": 11}]),
        ([{"id": 1, "name": "p_1", "price": 10}, {"id": 2, "name": "p_2", "price": 2}], [{"item_id": 1, "stock": 11}, {"item_id": 2, "stock": 2}], [{"id": 1, "name": "p_1", "price": 10, "stock": 11}, {"id": 2, "name": "p_2", "price": 2, "stock": 2}]),
    ])
def test_retain_only_items_in_stock(items, inventory, expected):
    actual = _retain_only_items_in_stock(items, inventory)
    assert actual == expected