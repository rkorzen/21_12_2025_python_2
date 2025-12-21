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
from collections import defaultdict

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

# 1. Łączna sprzedaż dla każdej kategorii

category_totals = defaultdict(int)

for item in sales:
    category = item["category"]
    quantity = item["quantity"]

    category_totals[category] += quantity

print("Łączna sprzedaż wg kategorii:")
for category, total in category_totals.items():
    print(f" - {category}: {total}")

# 2. Kategoria z najwyzsza sprzedażą

# top_category = None
# top_value = 0
#
# for category, total in category_totals.items():
#     if total > top_value:
#         top_category = category
#         top_value = total


def second(elem): return elem[1]
top_category = max(category_totals.items(), key=second)[0]
print("Kategoria z najwyższą sprzedażą to: ", top_category)

# 3. prodykty powyzej sredniej w swojej kategorii

category_counts = defaultdict(int)

for item in sales:
    category = item["category"]
    category_counts[category] += 1

# category_averages = {}
# for category, count in category_counts.items():
#     category_averages[category] = category_totals[category] / count

category_averages = {category: category_totals[category] / count for category, count in category_counts.items()}

print("Prodykty powyzej średniej w swojej kategorii: ")
for item in sales:
    product = item["product"]
    category = item["category"]
    quantity = item["quantity"]
    if quantity > category_averages[category]:
        print(f" - {product} ({category}, {quantity})")


# 4. produkty ze sprzedaza 0

zero_sales = []

for item in sales:
    if item["quantity"] == 0:
        zero_sales.append(item)

if zero_sales:
    print("Produkty z zerowa sprzedaza:")
    for item in zero_sales:
        print(f" - {item["product"]}")
else:
    print("Brak produktow z zerowa sprzedaza")

