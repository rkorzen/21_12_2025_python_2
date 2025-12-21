"""
## Zadanie 2: Analiza danych sprzedażowych

Dane sprzedażowe zapisane są jako lista słowników. Każdy element zawiera:

* nazwę produktu,
* kategorię produktu,
* liczbę sprzedanych sztuk.

```python
sales = [
    {"product": "Laptop", "category": "Electronics", "quantity": 15},
    {"product": "Mouse", "category": "Electronics", "quantity": 120},
    {"product": "Keyboard", "category": "Electronics", "quantity": 85},
    {"product": "Monitor", "category": "Electronics", "quantity": 0},
    {"product": "Desk", "category": "Furniture", "quantity": 20},
    {"product": "Chair", "category": "Furniture", "quantity": 55},
    {"product": "Lamp", "category": "Furniture", "quantity": 35},
    {"product": "Notebook", "category": "Office", "quantity": 200},
    {"product": "Pen", "category": "Office", "quantity": 350},
    {"product": "Stapler", "category": "Office", "quantity": 40},
]
```

### Twoim zadaniem jest:

1. Obliczyć łączną sprzedaż (sumę `quantity`) dla każdej kategorii.
2. Wypisać kategorię, która ma **najwyższą łączną sprzedaż**.
3. Wypisać wszystkie produkty, których sprzedaż jest **większa niż średnia sprzedaż w ich kategorii**.
4. Sprawdzić, czy istnieją produkty, których sprzedaż wynosi `0`, i wypisać ich nazwy (lub informację, że takich produktów nie ma).


"""