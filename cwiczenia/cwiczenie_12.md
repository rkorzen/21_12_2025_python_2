## Walka

#### Utwórz klasę Postac 

atrybuty:

    imie
    zdrowie
    max_zdrowie 
    _atak       - siła ataku uzytkownika 
    ekwipunek   - lista rzeczy

atrybut dynamiczny

    atak        - siła ataku wzbogacona o bonusy z przedmiotów

Postać powinna mieć metody:

    otrzymaj_obrazenia - pomniejsza zdrowie o podaną wartość
    wylecz             - powieksza zdrowie o podaną wartość (do max_zdrowie)
    daj_przedmiot      - dodaje przedmiot do ekwipunku
    zabierz_przedmiot  - usuwa przedmiot z ekwipunku
    czy_zyje           - jeśli zdrowie > 0 to żyje
    moc_ataku          - randomowa wartość całkowita z przedziału atak/2 do atak  



#### Utwórz klasę Przedmiot, 

atrybuty:

    nazwa, bonus_do_ataku

Jeśli przedmiot będzie w ekwipunku, to powiększa atak użytkownika


#### przykłady

    >>> rufus = Postac('Rufus', 35, 100)
    >>> tulipan = Przedmiot("Zielony tulipan zniszczenia", 5)
    >>> rufus.daj_przedmiot(tulipan)
    >>> print(rufus)

    Jestem Rufus, mam 35 ataku i 100/100 życia.
    EKWPIUNEK:
    Zielony tuplian zniszczenia, 5 do ataku



### Zdefiniuj funkcję walka

Walka toczy się na śmierć i życie. Przeciwnicy walczą dopóki żyją. 

walka odbywa się pomiędzy atakującym i broniącym, którzy uderzają się na przemian.
Przed każdym uderzeniem wyliczana jest moc_ataku, która jest losową liczbą z zakresu od 0.5 atak do atak

    >>> rufus = Postac("Rufus", 30, 100)
    >>> janusz = Postac("Janusz", 40, 120)

    >>> tulipan = Przedmiot("Zielony tuplian zniszczenia", 5)
    >>> rufus.daj_przedmiot(tulipan)

    >>> walka(rufus, janusz
)


Przykładowa walka:


    Walka: Rufus vs Janusz
    Jestem Rufus, mam 35 ataku i 100/100 życia.
    EKWPIUNEK:
    Zielony tuplian zniszczenia, 5 do ataku

    Jestem Janusz, mam 40 ataku i 120/120 życia.
    EKWPIUNEK:

    Rufus uderza Janusz za 20 obrażeń.
    Janusz oberwał za 20 obrażeń.
    Janusz uderza Rufus za 22 obrażeń.
    Rufus oberwał za 22 obrażeń.
    Jestem Rufus, mam 35 ataku i 78/100 życia.
    EKWPIUNEK:
    Zielony tuplian zniszczenia, 5 do ataku

    Jestem Janusz, mam 40 ataku i 100/120 życia.
    EKWPIUNEK:

    Rufus uderza Janusz za 32 obrażeń.
    Janusz oberwał za 32 obrażeń.
    Janusz uderza Rufus za 25 obrażeń.
    Rufus oberwał za 25 obrażeń.
    Jestem Rufus, mam 35 ataku i 53/100 życia.
    EKWPIUNEK:
    Zielony tuplian zniszczenia, 5 do ataku

    Jestem Janusz, mam 40 ataku i 68/120 życia.
    EKWPIUNEK:

    Rufus uderza Janusz za 31 obrażeń.
    Janusz oberwał za 31 obrażeń.
    Janusz uderza Rufus za 28 obrażeń.
    Rufus oberwał za 28 obrażeń.
    Jestem Rufus, mam 35 ataku i 25/100 życia.
    EKWPIUNEK:
    Zielony tuplian zniszczenia, 5 do ataku

    Jestem Janusz, mam 40 ataku i 37/120 życia.
    EKWPIUNEK:

    Rufus uderza Janusz za 31 obrażeń.
    Janusz oberwał za 31 obrażeń.
    Janusz uderza Rufus za 32 obrażeń.
    Rufus oberwał za 32 obrażeń.
    KONIEC WALKI
    Jestem Rufus, miałem 35 i nie żyję.
    Jestem Janusz, mam 40 ataku i 6/120 życia.
    EKWPIUNEK:




