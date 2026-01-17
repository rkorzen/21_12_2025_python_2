"""
Stworz klase reprezentujaca produkt

- id
- nazwe
- cene

Stworz klase BasketEntry zawierajaca:
- produkt
- ilosc

metoda:
calculate - oblicza wartosc pozycji w koszyku


$ python cwiczenia/cwiczenie_09.py
Witaj.

W ofercie posiadamy:
- Id: 1, Produkt: "Ogorek", cena: 5.34 PLN
- Id: 2, Produkt: "Kurczak", cena: 12.34 PLN
- Id: 3, Produkt: "Pizza", cena: 15.34 PLN

Co chcesz kupic (podaj id produktu lub q by zakonczyc)? 1
Ilosc: 2

Co chcesz kupic (podaj id produktu lub q by zakonczyc)? 2
Ilosc: 3

Co chcesz kupic (podaj id produktu lub q by zakonczyc)? q

Paragon:

Ogorek     ilosc: 2 cena: 10.68 PLN
Kurczak    ilosc: 3 cena: 37.02 PLN
-----------------------------------
Suma:                     47.70 PLN


"""


class Product:
    def __init__(self, id: int, name: str, price: float):
        self.id = id
        self.name = name
        self.price = price

    def info(self):
        return f'Id: {self.id}, Produkt: "{self.name}", cena: {self.price}'

    def __repr__(self):
        return f'<Produkt ({self.id}): {self.name} ({self.price} PLN)>'


class BasketEntry:
    def __init__(self, product: Product, quantity):
        self.product = product
        self.quantity = quantity

    def calculate(self):
        return self.product.price * self.quantity


class Basket:

    def __init__(self):
        self.entries: list[BasketEntry] = []

basket = Basket()
p = Product(1, "Ogorek", 5.34)
assert p.info() == 'Id: 1, Produkt: "Ogorek", cena: 5.34'
be = BasketEntry(p, 2)
basket.entries.append(be)
basket.entries.append("xxx")

for entry in basket.entries:
    print(entry)


### przydatne rzeczy:
"""
input
while


"""

