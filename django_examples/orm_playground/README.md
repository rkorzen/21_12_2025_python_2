# orm_playground

Projekt demonstracyjny Django 5.x pokazujący medium i advanced użycie ORM.

## Stack

- Python 3.12
- Django 5.x
- SQLite (domyślnie)
- PostgreSQL (opcjonalnie przez `docker-compose`)
- `pytest` + `pytest-django`
- `ruff` + `black`

## Quickstart

```bash
cd orm_playground
make init
make migrate
make seed
make run
```

Aplikacja raportowa będzie dostępna pod `http://127.0.0.1:8000/reports/`.

## Najważniejsze endpointy

- `/reports/top-products/?days=30&country=PL`
- `/reports/customers-ltv/?days=180&country=PL`
- `/reports/orders-with-late-payment/?days=60&grace_days=3`
- `/reports/events-matched-by-email/?days=30`
- `/reports/n-plus-one-demo/?limit=20`
- `/reports/window-rankings/?days=90`

Każdy endpoint zwraca:

- `description`
- `params`
- `results`
- `metrics` (w tym `query_count` przy `DEBUG=1`)

## Seed danych

Domyślnie komenda generuje:

- ~1200 osób
- ~600 produktów
- ~5000 zamówień
- ~30000 pozycji zamówień (zależnie od losowania)
- ~50000 event logów

Własne parametry:

```bash
uv run python manage.py seed --seed 123 --orders 5000 --event-logs 50000 --reset
```

## Pseudo-join bez FK

1. `Payment.external_order_ref` ↔ `Order.external_ref`
2. `EventLog.actor_email` ↔ `Person.email`
3. `InventorySnapshot.sku` ↔ `Product.sku`

Wykorzystane konstrukcje: `Subquery`, `OuterRef`, `Exists`, `Case/When`.

## PostgreSQL (opcjonalnie)

```bash
docker compose up -d
cp .env.example .env
export $(cat .env | xargs)
uv run python manage.py migrate
```

## Testy i lint

```bash
make test
make lint
```

## Dokumentacja ORM

- `docs/orm_medium.md`
- `docs/orm_advanced.md`
- `docs/modules/*.md`

## Import CSV/JSON (opcjonalnie)

```bash
uv run python manage.py import_data --entity people --path ./sample_people.csv
uv run python manage.py import_data --entity products --path ./sample_products.json
```
