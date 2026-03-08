# Django ORM na przykładzie raportów

Ten dokument wyjaśnia, jak działa ORM w tym projekcie na realnych funkcjach
z `reporting/services.py` i `reporting/views.py`.

## 1. Przepływ danych (request -> ORM -> odpowiedź)

Dla każdego raportu są dwie reprezentacje:

- JSON API, np. `/reports/top-products/`
- HTML, np. `/reports/html/top-products/`

Obie wersje używają tej samej funkcji budującej payload, np.
`_top_products_payload()` w `reporting/views.py`.

To oznacza:

- jedna logika parametryzacji i paginacji
- jeden queryset dla JSON i HTML
- prostsze utrzymanie (brak duplikacji zapytań)

## 2. Top products: `filter + values + annotate + order_by`

Kod źródłowy: `reporting/services.py:top_products_queryset`

Kluczowy fragment:

```python
revenue_expr = ExpressionWrapper(
    F("quantity") * F("unit_price"),
    output_field=DecimalField(max_digits=14, decimal_places=2),
)

return (
    OrderItem.objects.filter(filters)
    .values("product__sku", "product__name")
    .annotate(
        total_qty=Coalesce(Sum("quantity"), 0),
        revenue=Coalesce(Sum(revenue_expr), Value(Decimal("0.00"))),
        order_count=Count("order", distinct=True),
        avg_qty=Coalesce(Avg("quantity"), 0.0),
    )
    .order_by("-revenue", "product__sku")
)
```

Co tu się dzieje:

- `F(...)` i `ExpressionWrapper` liczą wartość pozycji po stronie SQL.
- `values(...)` grupuje wynik po produkcie (SKU, nazwa).
- `annotate(...)` dodaje agregaty (sumy, średnie, liczności).
- `Coalesce(...)` zabezpiecza `NULL` (np. brak danych) domyślną wartością.
- `order_by("-revenue", ...)` daje stabilny ranking.

## 3. Customers LTV: `FilteredRelation` i agregacja po relacji

Kod źródłowy: `reporting/services.py:customers_ltv_queryset`

Najważniejsza idea:

```python
queryset = Person.objects.active().annotate(
    scoped_orders=FilteredRelation("orders", condition=order_filters)
)
```

Po co:

- `FilteredRelation` tworzy alias relacji (`scoped_orders`) już z filtrem
  (okres, kraj).
- Dzięki temu `Sum(...)` i `Count(...)` liczą tylko zamówienia z tego zakresu,
  zamiast wszystkich zamówień klienta.

## 4. Late payments: pseudo-join bez FK (`OuterRef`, `Subquery`, `Exists`)

Kod źródłowy: `reporting/services.py:orders_with_late_payment_queryset`

Tu `Payment` nie ma klasycznego FK do `Order`, tylko referencję tekstową
`external_order_ref`. Dlatego jest pseudo-join:

```python
payments = Payment.objects.filter(
    external_order_ref=OuterRef("external_ref"),
    status=Payment.Status.PAID,
    paid_at__isnull=False,
).order_by("paid_at")
```

Następnie:

- `Subquery(...values("paid_at")[:1])` pobiera pierwszą płatność.
- `Exists(...)` sprawdza, czy płatność istnieje.
- `Case/When` wylicza flagę `late_payment`.

To wzorzec bardzo częsty przy integracjach między systemami, które łączą dane
po naturalnym kluczu (tu: `external_ref`), a nie po FK.

## 5. Events matched by email: adnotacje z custom QuerySet

Kod źródłowy:

- `events/models.py:EventLogQuerySet.with_actor_match`
- `reporting/services.py:events_matched_by_email_queryset`

Najpierw custom QuerySet (`with_actor_match`) dodaje:

- `has_person` (`Exists`)
- `matched_person_id` (`Subquery`)
- `matched_person_name` (`Subquery`)

Potem raport filtruje tylko dopasowane rekordy:

```python
return queryset.filter(has_person=True).order_by("-happened_at", "id")
```

## 6. Window functions: ranking i running total

Kod źródłowy: `reporting/services.py:window_rankings_queryset`

Najpierw liczymy `order_total` (Subquery z sumą pozycji zamówienia), potem:

- `Window(Rank())` -> ranking z remisami
- `Window(RowNumber())` -> numer porządkowy
- `Window(Sum("order_total"))` -> suma narastająca

To jest SQL-owe "okno" użyte bez surowego SQL, wprost przez ORM Django.

## 7. N+1: jak i dlaczego optymalizować relacje

Kod źródłowy:

- `serialize_orders_naive`
- `serialize_orders_optimized`
- `n_plus_one_demo`

Wersja naiwna iteruje po relacjach bez prefetch/select i generuje wiele zapytań.
Wersja zoptymalizowana:

- `select_related("customer__organization")` dla relacji 1-1 / FK
- `prefetch_related(Prefetch("items", queryset=...select_related("product")))`
  dla relacji 1-n

`CaptureQueriesContext` pokazuje różnicę liczby SQL-i w praktyce.

## 8. Jak to jest spięte z widokami HTML

Kod źródłowy: `reporting/views.py`

Kluczowe funkcje:

- `_..._payload(request)` -> wspólna logika raportu (parametry + ORM + paginacja)
- `_report_page(...)` -> uniwersalny renderer HTML (tabela, metryki, raw JSON)
- `_preset_links(...)` -> buduje "przyciski" z gotowymi parametrami

Przykład presetów:

```python
presets=[
    ("7 dni", {"days": 7, "page_size": 20}),
    ("30 dni PL", {"days": 30, "country": "PL", "page_size": 20}),
    ("90 dni US", {"days": 90, "country": "US", "page_size": 20}),
]
```

## 9. Checklist do pisania kolejnych raportów

1. Zdefiniuj queryset w `reporting/services.py`.
2. Użyj adnotacji/agregatów zamiast liczenia w Pythonie.
3. Dodaj stabilne `order_by(...)`.
4. Dodaj payload helper w `reporting/views.py`.
5. Podepnij endpoint JSON i stronę HTML z presetami.
6. Dodaj test dla HTML i/lub JSON.
