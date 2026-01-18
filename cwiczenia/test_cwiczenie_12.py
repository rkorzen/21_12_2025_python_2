from textwrap import dedent

import pytest
from cwiczenie_12 import Postac, Przedmiot, walka


def test_nowa_postac():
    postac = Postac(imie="A", atak=1, zdrowie=20)
    assert postac._atak == 1
    assert postac.zdrowie == 20
    assert postac.imie == "A"
    assert postac.max_zdrowie == 20


@pytest.fixture
def postac():
    return Postac(imie="A", atak=20, zdrowie=20)


@pytest.fixture
def przedmiot():
    return Przedmiot("Szparagi mocy", 30)


def test_postac_otrzymaj_obrazenia(postac):
    assert postac.zdrowie == 20
    assert postac.otrzymaj_obrazenia(10) is None
    assert postac.zdrowie == 10
    postac.otrzymaj_obrazenia(20)
    assert postac.zdrowie == 0


def test_postac_czy_zyje(postac):
    assert postac.czy_zyje() is True
    postac.zdrowie = 0
    assert postac.czy_zyje() is False


def test_postac_wylecz(postac):
    postac.zdrowie = 10
    postac.wylecz()
    assert postac.zdrowie == 20  # powrot do max_zdrowie
    postac.zdrowie = 0
    postac.wylecz()
    assert postac.zdrowie == 0


def test_postac_moc_ataku(postac, monkeypatch):
    def fake_random():
        return 0.5

    monkeypatch.setattr("cwiczenie_12.random", fake_random)

    assert postac.moc_ataku == 10


def test_postac_daj_przedmiot(postac):
    p = "xxx xxx"
    postac.daj_przedmiot(p)
    assert p in postac.ekwipunek


def test_postac_atak_bez_ekwipunku(postac, monkeypatch):
    def fake_random():
        return 0.5

    monkeypatch.setattr("cwiczenie_12.random", fake_random)

    assert postac.atak == 10


def test_postac_atak_z_ekwipunkiem(postac, przedmiot, monkeypatch):
    def fake_random():
        return 0.5

    monkeypatch.setattr("cwiczenie_12.random", fake_random)

    postac.daj_przedmiot(przedmiot)

    assert postac.atak == 10 + 30


def test_postac_bez_ekwipunku_str(postac):
    assert str(postac) == "Jestem A, mam 20 ataku i 20/20 życia."


def test_postac_z_ekwipunkiem_str(postac, przedmiot):
    postac.daj_przedmiot(przedmiot)

    expected = (
        "Jestem A, mam 20 ataku i 20/20 życia.\n"
        "EKWIPUNEK:\n"
        "Szparagi mocy, 30 do ataku\n"""
    )

    assert str(postac) == expected


def test_postac_zabierz_przedmiot(postac, przedmiot):
    postac.daj_przedmiot(przedmiot)
    assert przedmiot in postac.ekwipunek
    postac.zabierz_przedmiot(przedmiot)
    assert przedmiot not in postac.ekwipunek


def test_walka(capsys, monkeypatch):
    p1 = Postac("A", 10, 20)
    p2 = Postac("B", 10, 20)

    def fake_random():
        return 0.5

    monkeypatch.setattr("cwiczenie_12.random", fake_random)

    walka(p1, p2)

    captured = capsys.readouterr()

    assert captured.out == ('Jestem A, mam 10 ataku i 20/20 życia.\n'
                            '\n'
                            'Jestem B, mam 10 ataku i 20/20 życia.\n'
                            'A uderza B za 5 obrażeń.\n'
                            'B oberwał za 5 obrażeń.\n'
                            'B uderza A za 5 obrażeń.\n'
                            'A oberwał za 5 obrażeń.\n'

                            'Jestem A, mam 10 ataku i 15/20 życia.\n'
                            '\n'
                            'Jestem B, mam 10 ataku i 15/20 życia.\n'
                            'A uderza B za 5 obrażeń.\n'
                            'B oberwał za 5 obrażeń.\n'
                            'B uderza A za 5 obrażeń.\n'
                            'A oberwał za 5 obrażeń.\n'

                            'Jestem A, mam 10 ataku i 10/20 życia.\n'
                            '\n'
                            'Jestem B, mam 10 ataku i 10/20 życia.\n'
                            'A uderza B za 5 obrażeń.\n'
                            'B oberwał za 5 obrażeń.\n'
                            'B uderza A za 5 obrażeń.\n'
                            'A oberwał za 5 obrażeń.\n'

                            'Jestem A, mam 10 ataku i 5/20 życia.\n'
                            '\n'
                            'Jestem B, mam 10 ataku i 5/20 życia.\n'
                            'A uderza B za 5 obrażeń.\n'
                            'B oberwał za 5 obrażeń.\n'
                            
                            "KONIEC WALKI\n"
                            'Jestem B, miałem 20 i nie żyję.\n'
                            'Jestem A, mam 10 ataku i 5/20 życia.\n'

                            )
