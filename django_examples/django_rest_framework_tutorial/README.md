# cwiczenia

## stworz model Book w aplikacji books

satusy available, rent, archived

title: str
author: str
status: choices
visible: bool
created: datetime (auto_now_add=True)

## stworz serializer dla Book - zapisywanie i odczytywanie danych
po stworzeniu w shell utworz:

utworz ksiazke, zserializuj ksiazke, utworz ksiazke przy pomocy serializera, zserializuj wszystkie ksiazki...

## Stworz widok listy ksiazek (tylko GET)

## Obsluz tworzenie ksiazki przez API

pomoconiczo:

$ pip install httpie

http POST http://127.0.0.1:8000/api/books/ title="Krzyzacy" author="Henryl Sienkiewicz"