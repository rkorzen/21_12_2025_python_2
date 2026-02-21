Oprócz podstawowej konfiguracji projektu warto korzystać z dodatkowych narzędzi wspierających jakość kodu i testowanie.

**djlint**
Narzędzie do formatowania i lintowania szablonów Django (HTML/Jinja). Pomaga utrzymać spójny styl, poprawne wcięcia i czytelność template’ów.

Instalacja:

```
pip install djlint
```

Formatowanie szablonów dla Django:

```
djlint --profile=Django --reformat .
```

---

**pytest / pytest-django / pytest-cov**
Zestaw narzędzi do uruchamiania testów i mierzenia pokrycia kodu.

Instalacja:

```
pip install pytest pytest-cov pytest-django
```

Uruchomienie testów z pomiarem pokrycia:

```
pytest --cov
```

Generowanie raportu HTML z pokrycia:

```
coverage html
```

Raport będzie dostępny w katalogu `htmlcov/` (plik `index.html`).
