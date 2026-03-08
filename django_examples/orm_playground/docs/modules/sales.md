# Sales

- `Order`, `OrderItem`, `Payment`
- pseudo-join `Payment.external_order_ref` ↔ `Order.external_ref`
- `OrderQuerySet.with_order_total()`
- przykład `atomic + select_for_update` w `sales/services.py`
