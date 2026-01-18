from random import random


class Postac:

    def __init__(self, imie, atak, zdrowie):
        self.imie = imie
        self._atak = atak
        self.zdrowie = zdrowie
        self.max_zdrowie = zdrowie
        self.ekwipunek = []

    def otrzymaj_obrazenia(self, ilosc):
        self.zdrowie -= ilosc
        if self.zdrowie < 0:
            self.zdrowie = 0

    def czy_zyje(self):
        return self.zdrowie > 0

    def wylecz(self):
        if self.czy_zyje():
            self.zdrowie = self.max_zdrowie

    def daj_przedmiot(self, przedmiot):
        self.ekwipunek.append(przedmiot)

    def zabierz_przedmiot(self, przedmiot):
        if przedmiot in self.ekwipunek:
            self.ekwipunek.remove(przedmiot)

    @property
    def moc_ataku(self):
        """bazowa moc ataku postaci wyrazona jako liczba całkowita"""
        return int(self._atak * random())

    @property
    def atak(self):
        return self.moc_ataku + sum(p.bonus_ataku for p in self.ekwipunek)

    def __str__(self):
        if not self.czy_zyje():
            return f"Jestem {self.imie}, miałem {self.max_zdrowie} i nie żyję."

        result = f"Jestem {self.imie}, mam {self._atak} ataku i {self.zdrowie}/{self.max_zdrowie} życia."
        if self.ekwipunek:
            result += "\nEKWIPUNEK:\n"
            for przedmiot in self.ekwipunek:
                result += f"{przedmiot}\n"
        return result


class Przedmiot:
    def __init__(self, nazwa, bonus_ataku):
        self.nazwa = nazwa
        self.bonus_ataku = bonus_ataku

    def __str__(self):
        return f"{self.nazwa}, {self.bonus_ataku} do ataku"


def _cios(p1, p2):
    if p2.czy_zyje() and p1.czy_zyje():
        moc_ataku_p1 = p1.atak
        print(f"{p1.imie} uderza {p2.imie} za {moc_ataku_p1} obrażeń.")
        p2.otrzymaj_obrazenia(moc_ataku_p1)
        print(f"{p2.imie} oberwał za {moc_ataku_p1} obrażeń.")
    else:
        print("KONIEC WALKI")
        print(p1)
        print(p2)


def _runda(p1, p2):
    print(p1)
    print()
    print(p2)
    _cios(p1, p2)
    _cios(p2, p1)


def walka(p1: Postac, p2: Postac):
    while p1.czy_zyje() and p2.czy_zyje():
        _runda(p1, p2)
