# ORM Advanced (mapowanie do 12_djangom_orm_advanced.md)

## 1. `Subquery`, `OuterRef`, `Exists`

### Pseudo-join 1: Payment ↔ Order (bez FK)

Kod: `reporting/services.py:orders_with_late_payment_queryset()`

- `Payment.external_order_ref = OuterRef("external_ref")`
- `Subquery(...values("paid_at")[:1])` pobiera pierwszą płatność
- `Exists(...)` sprawdza istnienie płatności

### Pseudo-join 2: EventLog ↔ Person (bez FK)

Kod: `events/models.py:EventLogQuerySet.with_actor_match()` + endpoint `events_matched_by_email`

- dopasowanie po `actor_email` i `email`
- adnotacje `has_person`, `matched_person_id`, `matched_person_name`

### Pseudo-join 3: InventorySnapshot ↔ Product (bez FK)

Kod: `catalog/models.py:ProductQuerySet.with_latest_inventory_qty()`

- dopasowanie po `sku`
- `Subquery` zwraca najnowszy snapshot

## 2. Okna (`Window`, `Rank`, `RowNumber`, running totals)

Kod: `reporting/services.py:window_rankings_queryset()`

- rankowanie zamówień po wartości koszyka
- `row_number`
- skumulowany `running_total`

## 3. `prefetch_related(Prefetch(...queryset=...))`

Kod: `reporting/services.py:n_plus_one_demo()`

- prefetch pozycji zamówień z dodatkowym `select_related("product")`

## 4. `FilteredRelation`

Kod: `reporting/services.py:customers_ltv_queryset()`

- alias `scoped_orders` filtruje relację po okresie/kraju
- agregacja LTV liczona wyłącznie dla przefiltrowanych zamówień

## 5. Custom QuerySet + Manager

Kod:

- `people/PersonQuerySet`
- `catalog/ProductQuerySet`
- `sales/OrderQuerySet`
- `events/EventLogQuerySet`

## 6. Bulk operacje i pułapki

Kod: `core/management/commands/seed.py`

- `bulk_create`, `bulk_update`
- pułapka: brak wywołania `save()` i sygnałów podczas bulk

## 7. `defer`, `only`, `iterator`, `explain`

Przykłady shell:

```python
from sales.models import Order

Order.objects.only("id", "external_ref").iterator(chunk_size=1000)
Order.objects.defer("source_system_id").filter(status="confirmed")[:100]
Order.objects.filter(status="confirmed").explain()
```

## 8. GenericForeignKey

Kod: `events/models.py:EventLog`

- `content_type` + `object_id` + `content_object` umożliwiają podpięcie eventu do różnych modeli.
