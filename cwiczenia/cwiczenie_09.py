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
- Id: 1, Produkt: "Ogorek",   cena:  5.34 PLN
- Id: 2, Produkt: "Kurczak",  cena: 12.34 PLN
- Id: 3, Produkt: "Pizza",    cena: 15.34 PLN

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
from abc import ABC, abstractmethod
from textwrap import dedent


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
        self.entries: dict[int, BasketEntry] = {}

    def add_entry(self, product: Product, quantity: int):
        if product.id in self.entries:
            self.entries[product.id].quantity += quantity
        else:
            self.entries[product.id] = BasketEntry(product, quantity)

    def total_price(self):
        return sum(entry.calculate() for entry in self.entries.values())

    def _format_entry_line(self, entry: BasketEntry):
        return f"{entry.product.name:<10} ilosc: {entry.quantity:>3} cena: {entry.calculate():>7.2f} PLN"

    def _generate_entry_lines(self):
        lines = []
        for entry in self.entries.values():
            lines.append(self._format_entry_line(entry))
        return lines

    def _calculate_max_line_length(self, lines: list[str]):
        return max(len(l) for l in lines)

    def _format_total_line(self, total_price: float, max_lenght: int):
        len_tp = len(str(total_price)) + 5
        suma = f"Suma: {total_price:>{max_lenght - len_tp}.2f} PLN"
        return suma

    def _build_receipt_template(self, total_line):
        p = dedent(f"""
        Paragon:
        {{}}
        {'-' * 30}
        {total_line}""")
        return p

    def paragon(self):
        lines = self._generate_entry_lines()
        max_l = self._calculate_max_line_length(lines)

        tp = self.total_price()
        total_line = self._format_total_line(tp, max_l)

        receipt_template = self._build_receipt_template(total_line)
        receipt = receipt_template.format('\n'.join(lines))

        return receipt

    def print_receipt(self):
        print(self.paragon())


db = {
    1: Product(1, "Ogorek", 5.34),
    2: Product(2, "Kurczak", 12.34)
}

class IDbAdapter(ABC):

    @abstractmethod
    def get_product(self, id: int):
        pass

    @abstractmethod
    def get_products(self):
        pass

class DictDbAdapter(IDbAdapter):

    def __init__(self, db):
        self.db = db

    def get_product(self, id: int):
        return self.db[id]

    def get_products(self):
        return self.db.values()


class ShopService:
    def __init__(self, db: IDbAdapter):
        self.db = db

    def print_offert(self):
        print("Witaj.")
        print("W ofercie posiadamy:")
        for product in self.db.get_products():
            print(f" - {product.info()}")

    def run(self):
        self.print_offert()
        basket = Basket()
        while True:
            id = input("Co chcesz kupic (podaj id produktu lub q by zakonczyc)? ")
            if id == "q":
                break
            try:
                product = self.db.get_product(int(id))
                quantity = int(input(f"Ilosc: "))
                basket.add_entry(product, quantity)

            except ValueError:
                print("Podano nieprawidlowe dane.")

        basket.print_receipt()

def main():
    products = DictDbAdapter(db)
    service = ShopService(products)
    service.run()


if __name__ == "__main__":
    main()
