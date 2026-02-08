## instalacja

pip install django

albo

uv add install django


## tworzenie projektu

django-admin startproject nazwa_projektu

## uruchomienie serwera

python manage.py runserver


## tworzenie aplikacji:

 python manage.py startapp nazwa_aplikacji

## tworzenie migracji

python manage.py makemigrations

## wykonanie migracji

python manage.py migrate




## cwiczenia:

### 1 routing i views

Napisz widok (funkcja w views) i przypisz go do urla w glownym urls.py

http://127.0.0.1:8000/hello/  -> Hello Djano!

### 2. 

Utworz nowa aplikacje - matematyka

Utworz w niej urls i funkcje obslugujaca kalkulator z dowa argumentami

http://127.0.0.1:8000/matematyka/add/1/2/ -> 3
http://127.0.0.1:8000/matematyka/sub/1/2/ -> -1
http://127.0.0.1:8000/matematyka/mul/8/2/ -> 16

plus za wyodrebnienie logiki biznesowej (to co robi kalkulator) do osobnego modulu

(hint: utworz pl ik services.py w ktorym utworzysz MathService z odpowiednimi metodami)


### 3. 

Dopisz w aplikacji simplerouting model w ktorym bedziesz logowac uzycie username w widoku hello

class HelloUserNameHistory
    - username
    - date_of_use
    - user
    - ip_address

Dodaj model do Panel Admina
Pamietaj by zarejestrowac aplikacje w settings...

### cwiczenie - utrwalenie - apka, routing

1. Utworz nowa aplikacje - blog

zalozenie:

lista_postow = [{"id":1, "title": "A", "content": "tresc A"}, {"id": 2, "title": "B", "content": "tresc B"}]

/blog/ -> lista wszystkich wpisow (wyswietl liste)

na poczatek wypisz po prostu te liste:

tutaj szablon:

blog/templates/blog/list.html
    
[{"id":1, "title": "A", "content": "tresc A"}, {"id": 2, "title": "B", "content": "tresc B"}]


/blog/post/1

blog/templates/blog/post.html
{"id":1, "title": "A", "content": "tresc A"}



## Zadanie:

Dodaj aplikacje Books - analogiczna do bloga z wpisami

/books/ -> lista wszystkich ksiazek
/books/1 -> szczegoly ksiazki o id 1


Ksiazka ma:
- id
- title
- author
- content
- metode - length (powie ile ma znakow)


Stworz szablony, routing.
Dodaj do menu... 
zadbaj o uzycie {% url 'books:list' %}

dodaj paginacje
dodaj fabryke, ktora wytworzy zadana ilosc ksiazek z fake data


### Cwiczenie - szablony

stworz nowa aplikacje - aktualnosci

/aktualnosci/ -> lista wszystkich aktualnosci
/aktualnosci/1 -> szczegoly aktualnosci o id 1

zasymuluj dane z bazy danych przy pomocy listy obiektow typu News

klasa News:
- id
- title
- content
- is_published
- date_of_publication

Stworz szablony, gdzie w estetyczny sposob wyswietlisz prezentowane tresci (mozna w oparciu o bootstrap)
Dodaj routing i widoki dla tej aplikacji

dane utworz w osobnym module o nazwie services.py
tam utworz serwis

class DummyNewsService:

    def __init__(self, db):
        self.db = db

    def get_news(self):
        return ...

    def get_published_news(self):
        return ...

    def get_by_id(self, id):
        return ...


DummyNewsService(db=[News(), News()])

powyzszym serwisem posluguj sie w widokach


### cwiczeniwe - dodaj model News w aplikacji news (pola analogiczne do datclass - ale djangowo)

- id (doda automatycznie)
- title (max_length=200) VARCHAR(200) CharField(max_length=200)
- content (nie ma ograniczen) TEXT TextField()
- is_published (bool) BOOLEAN BooleanField() default=False
- date_of_publication  (date) DATE DateField(null=True)

- po dodaniu trzeba przygotowac i wykoanczyc migracje

  python manage.py makemigrations
  python manage.py migrate
  pyton manage.py shell

utworz news (3)
sprobu wybrac:
- wszystkie
- opublikowane
- po id

### cwiczenie - relacja one to many

dodaj TimeStampedModel do news.models i niech Autor i News dzeidzicza po tym 
(abstract=True)

Dodaj model Autor do aplikacji news
Autor ma:
- id
- first_name
- last_name
- birth_date  moze byc null
- death_date  moze byc null

dodanie relacji do autora do news
author = models.ForeignKey(Autor, on_delete=models.CASCADE, null=True)  # na poczatek moze byc puste
dodac related_name="news"

- zrobic migracje
- w shell dodac dane
- wyszukac wszystkie newsy danego autora


### relacja M2M

W aplikacji news dodaj model Tag
Tag ma:
- id
- name
- slug  SlugField - moze byc puste

trzeba dodac relacje m2m do news i autora

utworz migracje

dodaj jakies tagi do news i do autora

poszukaj autora po tagu

### PA - dodja modele news, author i tag do PA

## Dodaj dla Author w PA kolumne z licznikiem news tego autora

## Dodaj formularze w aplikacji news. Dla modelu Author i News - utworz instancje autora w shell przy pomocy formularza
   Zadbaj by imie, nazwisko zawsze zaczynalo sie wielka litera. Tak samo tytul newsa.
    
    data = {...}

    form = Form(data=data)

    form.is_valid():

    jesli sa bledy, czyli to co wyzej zwroci False

    form.errors
    form.save()


## utworz sciezke, widok do tworzenia autora

/news/authors/add - chcemy tu miec formularz do dodana autora. 