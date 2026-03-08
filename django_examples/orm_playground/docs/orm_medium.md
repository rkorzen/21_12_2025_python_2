# ORM Medium (mapowanie do 11_django_orm_medim.md)

## 1. `filter`, `exclude`, `Q`, `F`, `values`, `distinct`

Kod: `reporting/services.py` i modele `people/sales`.

- `top_products_queryset()` używa filtrów po okresie/kraju i `values(...)`.
- `orders_with_late_payment_queryset()` używa `Case/When` i porównań na polach.
- `OrderQuerySet.confirmed()` pokazuje czytelne enkapsulowanie filtrów biznesowych.

## 2. `select_related` vs `prefetch_related` + N+1

Kod: `reporting/services.py:n_plus_one_demo()`

- Wersja naiwna: iteracja po `Order` i dostęp do `customer`, `organization`, `items`, `product`.
- Wersja poprawna: `select_related("customer__organization")` + `Prefetch("items", queryset=...select_related("product"))`.

## 3. `annotate`, `aggregate`, `Coalesce`

Kod:

- `top_products_queryset()` (`Sum`, `Count`, `Avg`, `Coalesce`)
- `PersonQuerySet.with_total_spend()` (`Subquery` + agregacja)
- `OrderQuerySet.with_order_total()` (sumowanie pozycji zamówień)

## 4. Sortowanie, paginacja, stabilność

Kod: `reporting/views.py`

- Każdy endpoint ma `page` i `page_size`.
- Querysety mają stabilne `order_by` (np. po revenue i SKU).

## 5. Transakcje i blokady

Kod: `sales/services.py`

- `capture_payment_atomically()` demonstruje `transaction.atomic()` i `select_for_update()`.
- W SQLite `select_for_update()` nie wymusza realnej blokady wiersza (ważna uwaga szkoleniowa).

## 6. Constraints i indeksy

Przykłady:

- `sales/OrderItem`: ograniczenia ilości i rabatu
- `sales/Payment`: check kwoty i external ref
- `people/Person`: check email + indeksy po kraju/emailu
- `catalog/InventorySnapshot`: check non-negative + indeksy czasowe
