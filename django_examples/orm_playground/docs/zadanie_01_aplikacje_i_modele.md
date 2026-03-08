# Zadanie 01: Tworzenie aplikacji i modeli

## Cel zadania

Przygotuj szkielet projektu Django ORM, tworzac strukturę aplikacji i modeli
z tego repozytorium. To będzie baza do kolejnych zajęć z bardziej złożonych zapytań.

## Zakres

Masz utworzyć i skonfigurować aplikacje:

- `core`
- `people`
- `catalog`
- `sales`
- `events`
- `reporting`

Następnie dodaj je do `INSTALLED_APPS` i przygotuj modele opisane poniżej.

## Wymagane modele

## `core`

1. `TimeStampedModel` (abstrakcyjny):
- `created_at` (`DateTimeField`, domyślnie `timezone.now`)
- `updated_at` (`DateTimeField`, `auto_now=True`)

2. `SoftDeleteQuerySet`:
- `alive()`
- `deleted()`
- `soft_delete()`

3. `SoftDeleteManager`:
- domyślnie zwraca tylko rekordy aktywne (`is_deleted=False`)

## `people`

1. `Organization`
- `name`, `country_code`, `source_system_id`
- unikalność: (`name`, `country_code`)
- indeksy: (`country_code`, `name`), (`source_system_id`)

2. `Role`
- `code` (unikalne), `label`

3. `Person`
- `email` (unikalne), `full_name`
- FK do `Organization` (`on_delete=PROTECT`, `related_name="people"`)
- self FK `manager` (`SET_NULL`, `null=True`, `blank=True`, `related_name="reports"`)
- `country_code`, `is_active`, `is_deleted`, `source_system_id`, `joined_at`
- M2M do `Role` przez `PersonRole`
- custom manager: `PersonQuerySet`
- indeksy: (`country_code`, `email`), (`source_system_id`)
- check constraint: email zawiera `@`

4. `PersonRole` (tabela pośrednia)
- FK do `Person`, FK do `Role`
- FK do `Organization` (`null=True`, `blank=True`)
- `assigned_at`, `source_system_id`
- unikalność: (`person`, `role`, `organization`)
- indeks: (`source_system_id`)

5. `PersonQuerySet`
- `active()`
- `in_country(country_code)`
- `with_total_spend()` (adnotacja sumy wydatków klienta na podstawie `sales.OrderItem`)

## `catalog`

1. `Category`
- `name`
- self FK `parent` (`SET_NULL`, `null=True`, `blank=True`, `related_name="children"`)
- unikalność: (`name`, `parent`)
- indeks: (`name`)

2. `Tag`
- `name` (unikalne)

3. `Product`
- `sku` (unikalne), `name`
- FK do `Category` (`PROTECT`, `related_name="products"`)
- M2M do `Tag` (`related_name="products"`, `blank=True`)
- `base_price`, `country_code`, `source_system_id`, `is_active`
- custom manager: `ProductQuerySet`
- indeksy: (`sku`, `country_code`), (`source_system_id`)
- check constraint: `base_price >= 0`

4. `InventorySnapshot`
- `sku`, `captured_at`, `available_qty`, `reserved_qty`, `warehouse_code`
- indeksy: (`sku`, `-captured_at`), (`warehouse_code`)
- check constraints: `available_qty >= 0`, `reserved_qty >= 0`

5. `ProductQuerySet`
- `active()`
- `with_latest_inventory_qty()` (adnotacja najnowszego stanu magazynu po `sku`)

## `sales`

1. `Order`
- `external_ref` (unikalne)
- FK `customer` do `people.Person` (`PROTECT`, `related_name="orders"`)
- `status` (`draft`, `confirmed`, `shipped`, `cancelled`)
- `country_code`, `source_system_id`
- custom manager: `OrderQuerySet`
- indeksy: (`created_at`, `status`), (`source_system_id`)
- check constraint: `external_ref` nie może być pusty

2. `OrderItem`
- FK do `Order` (`related_name="items"`)
- FK do `catalog.Product` (`PROTECT`, `related_name="order_items"`)
- `quantity`, `unit_price`, `discount_pct`
- unikalność: (`order`, `product`)
- check constraints: `quantity > 0`, `unit_price >= 0`, `discount_pct` w zakresie `0..100`
- indeks: (`order`, `product`)

3. `Payment`
- `external_order_ref`, `status`, `amount`, `paid_at`, `provider`, `transaction_id`, `source_system_id`
- `transaction_id` unikalne
- indeksy: (`external_order_ref`, `status`), (`paid_at`), (`source_system_id`)
- check constraints: `amount >= 0`, `external_order_ref` niepuste
- Uwaga: tu **nie ma FK** do `Order` (łączenie po `external_order_ref` ↔ `external_ref`)

4. `OrderQuerySet`
- `confirmed()`
- `in_country(country_code)`
- `with_order_total()` (adnotacja sumy pozycji zamówienia)

## `events`

1. `EventLog`
- `actor_email`, `event_type`, `happened_at`, `payload`, `country_code`, `source_system_id`
- `event_type`: `login`, `order_placed`, `payment_updated`, `profile_updated`
- `GenericForeignKey` (`content_type`, `object_id`, `content_object`)
- custom manager: `EventLogQuerySet`
- indeksy: (`actor_email`, `happened_at`), (`event_type`, `happened_at`), (`source_system_id`)
- check constraint: `actor_email` puste albo zawiera `@`

2. `EventLogQuerySet`
- `with_actor_match()`:
  - dopasowuje aktora do `people.Person` po e-mailu
  - adnotuje: `has_person`, `matched_person_id`, `matched_person_name`

## `reporting`

- Na tym etapie bez modeli trwałych (aplikacja będzie służyć do zapytań i raportów).

## Relacje, które muszą działać

- `Organization (1) -> (N) Person`
- `Person (1) -> (N) Order`
- `Order (1) -> (N) OrderItem`
- `Product (1) -> (N) OrderItem`
- `Category (1) -> (N) Product`
- `Category (1) -> (N) Category` przez `parent`
- `Person (N) <-> (N) Role` przez `PersonRole`
- `Product (N) <-> (N) Tag`
- `Person (1) -> (N) Person` przez `manager`

Pseudo-joiny (bez FK, wymagane do dalszych ćwiczeń):

- `Payment.external_order_ref` ↔ `Order.external_ref`
- `EventLog.actor_email` ↔ `Person.email`
- `InventorySnapshot.sku` ↔ `Product.sku`

## Kryteria zaliczenia

1. Wszystkie aplikacje istnieją i są dodane do `INSTALLED_APPS`.
2. Wszystkie modele i relacje są utworzone.
3. Działają custom QuerySety:
- `PersonQuerySet`
- `ProductQuerySet`
- `OrderQuerySet`
- `EventLogQuerySet`
4. Są dodane wymagane indeksy i constraints.
5. Migracje tworzą schemat bez błędów.

## Komendy kontrolne

```bash
uv run python manage.py makemigrations
uv run python manage.py migrate
uv run python manage.py check
```

## Dla chętnych

1. Dodaj czytelne `__str__` dla wszystkich modeli.
2. Dodaj krótkie docstringi opisujące rolę modelu.
3. Zweryfikuj strukturę przez uruchomienie `uv run pytest`.
