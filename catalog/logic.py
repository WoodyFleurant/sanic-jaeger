def _retain_only_items_in_stock(items, inventory):
    retained_items = []
    for item in items:
        inventory_item = _get_inventory_for_item(item, inventory)
        if inventory_item and inventory_item["stock"] > 0:
            retained_items.append({
                "id": item["id"],
                "name": item["name"],
                "price": item["price"],
                "stock": inventory_item["stock"]
            })
    return retained_items


def _get_inventory_for_item(item, inventory):
    for inventory_item in inventory:
        if item["id"] == inventory_item["item_id"]:
            return inventory_item
    return None
