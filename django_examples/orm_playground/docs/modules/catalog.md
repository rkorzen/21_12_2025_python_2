# Catalog

- `Category` (self relation `parent`)
- `Product`, `Tag`
- `InventorySnapshot` bez FK do `Product` (join po `sku`)
- custom `ProductQuerySet.with_latest_inventory_qty()`
