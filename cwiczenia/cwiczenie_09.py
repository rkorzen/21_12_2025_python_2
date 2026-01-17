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

"""

class Product:
    def __init__(self, id, name, price):
        self.id = id
        self.name = name
        self.price = price

    def info(self):
        return f'Id: {self.id}, Produkt: "{self.name}", cena: {self.price}'

    def __repr__(self):
        return f'<Produkt ({self.id}): {self.name} ({self.price} PLN)>'

basket = []
p = Product(1, "Ogorek", 5.34)
assert p.info() == 'Id: 1, Produkt: "Ogorek", cena: 5.34'

basket.append(p)
print(p)
print(basket)