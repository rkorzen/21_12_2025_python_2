"""
# Zadanie - funkcje - adv

## System naliczania prowizji sprzedażowych (wersja rozszerzona)

### Kontekst biznesowy

Firma sprzedażowa wypłaca prowizje handlowcom.
Prowizja zależy od:

* wartości sprzedaży,
* regionu sprzedaży,
* typu klienta,
* aktualnej polityki prowizyjnej (strategii),
* dodatkowych modyfikatorów (np. premie kwartalne).

System musi być:

* **elastyczny** (łatwa zmiana reguł),
* **testowalny**,
* **otwarty na rozbudowę bez modyfikowania głównej logiki**.

---

### Dane wejściowe

```python
sales = [
    {"seller": "Anna", "region": "EU", "client_type": "B2B", "amount": 120_000},
    {"seller": "Anna", "region": "EU", "client_type": "B2C", "amount": 15_000},
    {"seller": "Anna", "region": "US", "client_type": "B2B", "amount": 90_000},

    {"seller": "Bartek", "region": "US", "client_type": "B2C", "amount": 8_000},
    {"seller": "Bartek", "region": "EU", "client_type": "B2C", "amount": 22_000},

    {"seller": "Celina", "region": "EU", "client_type": "B2B", "amount": 250_000},
    {"seller": "Celina", "region": "ASIA", "client_type": "B2B", "amount": 60_000},

    {"seller": "Daniel", "region": "ASIA", "client_type": "B2C", "amount": 12_000},
    {"seller": "Daniel", "region": "EU", "client_type": "B2C", "amount": 9_000},
]
```

---

### Zasady biznesowe

1. **Bazowa prowizja**

   * 5% od kwoty sprzedaży

2. **Modyfikator regionu**

   * EU → +1%
   * US → +2%
   * ASIA → +3%

3. **Modyfikator typu klienta**

   * B2B → +2%
   * B2C → 0%

4. **Premia za wysoką sprzedaż**

   * jeśli `amount > 100_000` → +1% (opcjonalny modyfikator)

---

### Wymagania techniczne

* zastosuj **funkcje jako obiekty pierwszej klasy**:

  * funkcje modyfikujące prowizję przekazywane jako argumenty,
* użyj:

  * parametrów pozycyjnych i nazwanych,
  * wartości domyślnych,
  * `*args` dla listy modyfikatorów,
* główna funkcja licząca prowizje **nie może znać szczegółów reguł**,
* wynik: **łączna prowizja per sprzedawca**.


"""
from collections import defaultdict

sales = [
    {"seller": "Anna", "region": "EU", "client_type": "B2B", "amount": 120_000},
    {"seller": "Anna", "region": "EU", "client_type": "B2C", "amount": 15_000},
    {"seller": "Anna", "region": "US", "client_type": "B2B", "amount": 90_000},

    {"seller": "Bartek", "region": "US", "client_type": "B2C", "amount": 8_000},
    {"seller": "Bartek", "region": "EU", "client_type": "B2C", "amount": 22_000},

    {"seller": "Celina", "region": "EU", "client_type": "B2B", "amount": 250_000},
    {"seller": "Celina", "region": "ASIA", "client_type": "B2B", "amount": 60_000},

    {"seller": "Daniel", "region": "ASIA", "client_type": "B2C", "amount": 12_000},
    {"seller": "Daniel", "region": "EU", "client_type": "B2C", "amount": 9_000},
]

REGION_MODIFIERS = {"EU": 0.01, "US": 0.02, "ASIA": 0.03}
CLIENT_TYPE_MODIFIERS = {"B2B": 0.02, "B2C": 0}


def base_commission(sale):
    return sale["amount"] * 0.05


modifiers = [base_commission]

def register(func):
    if func not in modifiers:
        modifiers.append(func)
    return func

@register
def region_modifier(sale):
    """Regionalna prowizja"""
    region = sale["region"]
    return sale["amount"] * REGION_MODIFIERS[region]

# region_modifier = register(region_modifier)


@register
def client_type_modifier(sale):
    client_type = sale["client_type"]
    return sale["amount"] * CLIENT_TYPE_MODIFIERS[client_type]

@register
def high_amount_modifier(sale):
    if sale["amount"] > 100_000:
        return 0.01 * sale["amount"]
    return 0.0

def apply_modifiers(sale, result):
    for modifier in modifiers:
        result[sale["seller"]] += modifier(sale)
    return result

def calculate_commissions(sales, modifiers):
    result = defaultdict(float)

    for sale in sales:
        # tutaj bede chcial policzyc dla poszczegolnych sale jak to powinno wygladac
        result = apply_modifiers(sale, result)

    return result

def present_resultset(resultset):
    for seller, commission in resultset.items():
        print(f"{seller}: {commission:.2f}")

if __name__ == "__main__":
    resultset = calculate_commissions(sales, modifiers)
    present_resultset(resultset)
