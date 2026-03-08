# Wytyczne prowadzacego: ORM Medium -> ORM Advanced

## Cel

Poprowadzic material tak, aby kazdy kolejny element ORM wynikal z poprzedniego:

1. najpierw czytelne query i agregacje,
2. potem optymalizacja i enkapsulacja,
3. na koncu pseudo-joiny, okna i wzorce "produkcyjne".

## Zasada prowadzaca

Za kazdym razem, gdy wprowadzasz nowa technike, powiedz wprost 4 rzeczy:

1. Po co jej uzywamy (problem biznesowy/wydajnosciowy).
2. Co ORM wygeneruje w SQL (JOIN, GROUP BY, subquery, window).
3. Jaki jest koszt/pulapka (N+1, duplikaty, NULL, zly order, lock).
4. Dlaczego to jest lepsze niz alternatywa "w Pythonie".

## Przygotowanie przed lekcja

Uruchom:

```bash
uv run python manage.py migrate
uv run python manage.py seed --seed 123 --reset
uv run python manage.py runserver
```

W trakcie pokazu korzystaj z endpointow `/reports/...` i kodu z `reporting/services.py`.

## Kolejnosc prowadzenia (jedno wynika z drugiego)

## Blok 1: ORM Medium

1. QuerySet API: `filter`, `exclude`, `Q`
- Gdzie: `top_products_queryset`, `customers_ltv_queryset`, `OrderQuerySet.confirmed`.
- Co pokazac: skladanie warunkow, dodawanie filtra `country` warunkowo.
- Co powiedziec: QuerySet jest leniwy. `Q` pozwala skladac logike warunkow, zamiast pisac kilka ifow i petli.
- Dlaczego teraz: to baza dla wszystkich kolejnych krokow.

2. Operacje na polach: `F` + `ExpressionWrapper`
- Gdzie: `top_products_queryset` (`quantity * unit_price`).
- Co pokazac: liczenie revenue po stronie SQL, nie w Pythonie.
- Co powiedziec: `F` odwoluje sie do kolumny bazy. `ExpressionWrapper` jawnie ustawia typ wyniku, zeby ORM i DB nie zgadywaly.
- Przejscie: skoro umiemy liczyc na kolumnach, mozemy agregowac.

3. Grupowanie i agregacje: `values`, `annotate`, `aggregate`, `Count`, `Sum`, `Avg`
- Gdzie: `top_products_queryset`.
- Co pokazac: ranking produktow i liczbe zamowien.
- Co powiedziec: `values(...)` ustawia klucz grupowania, `annotate(...)` liczy metryki dla grup. To jest odpowiednik `GROUP BY`.
- Przejscie: agregacje sa poprawne, ale musimy obsluzyc braki danych.

4. `Coalesce` i semantyka `NULL`
- Gdzie: `top_products_queryset`, `customers_ltv_queryset`, `window_rankings_queryset`.
- Co pokazac: domyslna wartosc `0` dla pustych agregatow.
- Co powiedziec: `NULL` rozwala dalsze obliczenia i sortowanie. `Coalesce` daje przewidywalny typ i wartosc.
- Przejscie: kiedy wynik jest stabilny, mozemy go bezpiecznie sortowac i stronicowac.

5. Stabilne sortowanie i paginacja
- Gdzie: `order_by(...)` w querysetach + `paginate_queryset`.
- Co pokazac: drugie pole sortowania (np. `sku`, `id`) dla stabilnosci.
- Co powiedziec: bez stabilnego `order_by` strony paginacji moga "plywac" miedzy zapytaniami.
- Przejscie: zapytania sa czytelne, ale czesto sa za wolne przez relacje.

6. N+1 i relacje: `select_related` vs `prefetch_related`
- Gdzie: `serialize_orders_naive`, `serialize_orders_optimized`, `n_plus_one_demo`.
- Co pokazac: roznice `bad_query_count` vs `good_query_count`.
- Co powiedziec: `select_related` jest dla FK/one-to-one (JOIN), `prefetch_related` dla relacji wielowartosciowych (osobne zapytanie + mapowanie).
- Przejscie: skoro znamy optymalizacje, mozemy przeniesc logike do API domenowego.

7. Custom QuerySet/Manager jako API domenowe
- Gdzie: `PersonQuerySet`, `ProductQuerySet`, `OrderQuerySet`, `EventLogQuerySet`.
- Co pokazac: `Order.objects.confirmed().in_country("PL")`.
- Co powiedziec: to nie "sztuka dla sztuki", tylko redukcja duplikacji i mniej bledow w filtrach biznesowych.
- Przejscie do advanced: mamy solidna baze, teraz laczymy dane bez klasycznych FK.

8. Transakcje i blokady (`atomic`, `select_for_update`)
- Gdzie: `sales/services.py`.
- Co pokazac: dlaczego update platnosci powinien byc atomowy.
- Co powiedziec: transakcja gwarantuje spojny zapis. `select_for_update` chroni przed race condition (w SQLite ograniczenie, w Postgres realny lock).
- Domkniecie medium: od tej chwili kursanci umieja pisac poprawne i wydajne raporty.

## Blok 2: ORM Advanced

9. Pseudo-join bez FK: `OuterRef`, `Subquery`, `Exists`
- Gdzie: `orders_with_late_payment_queryset`.
- Co pokazac: powiazanie `Payment.external_order_ref` z `Order.external_ref`.
- Co powiedziec: `OuterRef` odwoluje sie do pola "zewnetrznego" rekordu. `Subquery` zwraca wartosc z podzapytania, `Exists` daje szybki bool.
- Przejscie: skoro juz umiemy pobrac powiazane dane, mozemy na nich budowac logike warunkowa.

10. Warunki w SQL: `Case/When`
- Gdzie: `orders_with_late_payment_queryset` (`late_payment`).
- Co pokazac: flaga opoznionej platnosci liczona po stronie bazy.
- Co powiedziec: `Case/When` to if/else w SQL. Dzieki temu filtrujesz po gotowej adnotacji bez obrobki w Pythonie.
- Przejscie: mamy warunkowe adnotacje, teraz zawezamy relacje "w miejscu".

11. `FilteredRelation`
- Gdzie: `customers_ltv_queryset` (`scoped_orders`).
- Co pokazac: LTV z zamowien tylko z okresu/kraju.
- Co powiedziec: `FilteredRelation` tworzy alias relacji juz z warunkiem, wiec agregacja liczy dokladnie to, co trzeba.
- Przejscie: po agregacjach i subquery czas na analityke rankingowa.

12. Funkcje okna: `Window`, `Rank`, `RowNumber`, running total
- Gdzie: `window_rankings_queryset`.
- Co pokazac: roznice miedzy `rank` i `row_number` oraz `running_total`.
- Co powiedziec: okna nie redukuja liczby wierszy jak `GROUP BY`; dodaja metryki "przez przekroj" wyniku.
- Przejscie: kursanci widza juz wzorce BI/analityczne w ORM.

13. `GenericForeignKey`
- Gdzie: `events/models.py` (`EventLog`).
- Co pokazac: event moze wskazywac rozne typy obiektow.
- Co powiedziec: GFK daje elastycznosc modelowania zdarzen, ale wymaga ostroznosci przy raportowaniu i indeksowaniu.
- Przejscie: konczymy tematami wydajnosci i utrzymania.

14. Bulk operacje i narzedzia diagnostyczne
- Gdzie: `core/management/commands/seed.py` + shell (`only`, `defer`, `iterator`, `explain`).
- Co pokazac: `bulk_create` jest szybkie, ale omija `save()` i sygnaly.
- Co powiedziec: optymalizacja to kompromis. Najpierw poprawna logika, potem pomiar i tuning.

## Co powiedziec, gdy uzywasz danej techniki (sciaga)

- `Q`: "Skladam warunki dynamicznie, nadal jako jedno zapytanie SQL."
- `F`: "Porownuje/licze na kolumnach w bazie, nie sciagam danych do Pythona."
- `annotate`: "Dodaje obliczone kolumny do kazdego rekordu wyniku."
- `aggregate`: "Zwracam jedna paczke metryk dla calego querysetu."
- `Coalesce`: "Zamieniam NULL na wartosc domyslna, zeby wynik byl stabilny."
- `select_related`: "JOIN dla pojedynczej relacji (FK/OneToOne)."
- `prefetch_related`: "Dodatkowe zapytanie i sklejenie w pamieci dla relacji wielowartosciowych."
- `OuterRef`: "Pole z zapytania zewnetrznego uzyte w podzapytaniu."
- `Subquery`: "Wartosc wyliczona podzapytaniem jako kolumna."
- `Exists`: "Szybki test istnienia rekordu spelniajacego warunek."
- `Case/When`: "Logika warunkowa if/else wykonana po stronie SQL."
- `FilteredRelation`: "Relacja z warunkiem, zeby agregowac tylko wlasciwy podzbior."
- `Window`: "Analityka po wierszach bez utraty szczegolow rekordu."
- `atomic`: "Albo zapisuje sie wszystko, albo nic."
- `select_for_update`: "Blokuje rekord do konca transakcji, zeby uniknac wyscigu."

## Sugestia czasowa

1. Blok medium: 90 min.
2. Przerwa + Q&A: 15 min.
3. Blok advanced: 90 min.
4. Podsumowanie i mini-zadanie: 20 min.

## Mini-zadanie na koniec (spina oba poziomy)

Polecenie dla kursantow:

1. Zbuduj raport "Top organizacje po LTV" dla `days` i `country`.
2. Uzyj: `FilteredRelation`, `annotate`, stabilne `order_by`, paginacje.
3. Dodaj wariant "advanced": flaga `has_late_payment` liczona przez `Exists` + `Subquery`.

Efekt: kursanci lacza medium i advanced w jednym, realistycznym query.
