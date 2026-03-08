# General View projektu `orm_playground`

Ten dokument to mapa calego projektu dla kursantow. Celem jest szybkie
zrozumienie:

- po co istnieja poszczegolne aplikacje,
- jakie modele sa w kazdej aplikacji,
- co z czym jest powiazane,
- jak dane plyna od seedowania do raportow JSON/HTML.

## 1. Po co jest ten projekt

`orm_playground` to laboratorium Django ORM. Nie jest to "pelny sklep", tylko
kontrolowane srodowisko do nauki:

- zapytan prostych i zaawansowanych,
- agregacji i adnotacji,
- pseudo-joinow bez klasycznych FK,
- optymalizacji zapytan (N+1, `select_related`, `prefetch_related`),
- prezentacji wynikow jako API i HTML.

## 2. Dlaczego podzial na takie aplikacje

Podzial odzwierciedla domene i odpowiedzialnosci:

1. `core`
- rzeczy wspolne dla calego projektu: modele bazowe, narzedzia, komendy.
- tu jest m.in. `TimeStampedModel`, `seed`, `import_data`, strona glowna.

2. `people`
- kontekst "kto": osoby, organizacje, role i struktura manager->pracownik.
- to zrodlo danych "klienci/uzytkownicy".

3. `catalog`
- kontekst "co sprzedajemy": produkty, kategorie, tagi, snapshoty magazynu.

4. `sales`
- kontekst "co kupiono i za ile": zamowienia, pozycje zamowien, platnosci.

5. `events`
- kontekst "co sie wydarzylo": logi zdarzen technicznych/biznesowych.

6. `reporting`
- warstwa odczytowa: laczy dane z wielu aplikacji i buduje raporty.
- trzyma logike zapytan i prezentacje (JSON + HTML z presetami).

Taki podzial pomaga uczyc sie ORM "po kawalkach", a jednoczesnie pokazuje
realna wspolprace modulow.

## 3. Modele i ich rola

## `core`

- `TimeStampedModel` (abstrakcyjny): wspolne pola `created_at`, `updated_at`.
- `SoftDeleteQuerySet` + `SoftDeleteManager`: wzorzec "soft delete".

## `people`

- `Organization`: firma/oddzial, do ktorej nalezy osoba.
- `Role`: slownik rol biznesowych.
- `Person`: osoba z e-mailem, krajem, managerem i organizacja.
- `PersonRole`: relacja M2M Person <-> Role z kontekstem organizacji.
- `PersonQuerySet`: helpery domenowe (`active`, `in_country`, `with_total_spend`).

## `catalog`

- `Category`: drzewo kategorii (self FK `parent`).
- `Tag`: etykiety produktowe.
- `Product`: karta produktu (SKU, cena, kraj, aktywnosc).
- `InventorySnapshot`: snapshot stanu magazynu po `sku`.
- `ProductQuerySet`: helpery (`active`, `with_latest_inventory_qty`).

## `sales`

- `Order`: naglowek zamowienia klienta.
- `OrderItem`: pozycja zamowienia (produkt, ilosc, cena, rabat).
- `Payment`: zdarzenie platnicze, laczone z zamowieniem przez `external_order_ref`.
- `OrderQuerySet`: helpery (`confirmed`, `in_country`, `with_order_total`).

## `events`

- `EventLog`: wpis zdarzenia (aktor, typ, payload, czas).
- `EventLogQuerySet`: helper `with_actor_match` (dopasowanie do `Person` po e-mailu).
- `GenericForeignKey` pozwala wskazac rozne obiekty (np. Person/Order/Product).

## `reporting`

- brak trwalych modeli.
- aplikacja sklada dane z pozostalych aplikacji i buduje raporty.

## 4. Co z czym sie wiaze (mapa relacji)

Relacje "klasyczne" (FK/M2M):

- `Organization (1) -> (N) Person`
- `Person (1) -> (N) Order` (`Order.customer`)
- `Order (1) -> (N) OrderItem`
- `Product (1) -> (N) OrderItem`
- `Category (1) -> (N) Product`
- `Category (1) -> (N) Category` przez `parent`
- `Person (N) <-> (N) Role` przez `PersonRole`
- `Product (N) <-> (N) Tag`
- `Person (1) -> (N) Person` przez `manager` (self-FK)

Relacje "integracyjne" (pseudo-join, bez FK):

- `Payment.external_order_ref` <-> `Order.external_ref`
- `EventLog.actor_email` <-> `Person.email`
- `InventorySnapshot.sku` <-> `Product.sku`

To celowy zabieg szkoleniowy: pokazuje, jak laczyc dane z systemow, ktore nie
maja idealnych kluczy obcych.

## 5. Dlaczego sa tez pseudo-joiny

W realnych systemach dane czesto przychodza z wielu zrodel:

- system zamowien,
- bramka platnosci,
- tracker eventow,
- system magazynowy.

Nie zawsze mamy FK miedzy tabelami. Dlatego projekt pokazuje wzorce ORM:

- `OuterRef`,
- `Subquery`,
- `Exists`,
- `Case/When`.

Dzieki temu kursanci ucza sie nie tylko "idealnego" modelu SQL, ale tez
integracji danych w warunkach produkcyjnych.

## 6. Jak dane pojawiaja sie w projekcie (seed)

Komenda `seed` buduje spojna historie danych:

1. `people`: organizacje, role, osoby, przypisania rol.
2. `catalog`: kategorie, tagi, produkty, snapshoty magazynowe.
3. `sales`: zamowienia, pozycje i platnosci.
4. `events`: logi zdarzen, czesc dopasowalna po e-mailu.

Wazne: dane sa generowane deterministycznie po podaniu `--seed`, co ulatwia
porownywanie wynikow zapytan i cwiczenia.

## 7. Jak dziala warstwa raportowa

`reporting/services.py` zawiera query logic (ORM), a `reporting/views.py`
prezentuje wynik na dwa sposoby:

- JSON API: endpointy `/reports/...`
- HTML: endpointy `/reports/html/...` + przyciski presetow parametrow

Czyli jedna logika danych, dwie formy prezentacji.

To wazne dydaktycznie:

- JSON dobrze pokazuje surowa strukture,
- HTML ulatwia "wizualne" porownanie wariantow parametrow.

## 8. Jak to czytac jako kursant (sugerowana sciezka)

1. Zacznij od `people`, `catalog`, `sales`, `events` i przeczytaj modele.
2. Zobacz custom QuerySety/manager-y i zrozum, czemu filtry sa tam.
3. Przejdz do `reporting/services.py` i analizuj zapytania krok po kroku.
4. Uruchamiaj raporty HTML i klikaj presety, porownujac wyniki.
5. Dopiero potem przejdz do wersji advanced (`Subquery`, `Window`, pseudo-join).

## 9. Najwazniejsza idea architektoniczna

Projekt rozdziela:

- model domeny (aplikacje `people/catalog/sales/events`),
- logike raportowa (`reporting/services.py`),
- transport/prezentacje (`reporting/views.py`, JSON/HTML).

Dzieki temu kazda warstwa jest czytelna, testowalna i dobrze nadaje sie do
nauki ORM na realistycznym, ale kontrolowanym przykladzie.
