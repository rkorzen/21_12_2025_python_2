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

(hint: utworz plik services.py w ktorym utworzysz MathService z odpowiednimi metodami)