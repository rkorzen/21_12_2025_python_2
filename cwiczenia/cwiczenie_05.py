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