"""

## Zadanie 3: Analiza aktywności użytkowników (login / logout + czas)

Dane aktywności użytkowników zapisane są jako lista zdarzeń.
Każde zdarzenie zawiera:

* identyfikator użytkownika (`user_id`),
* typ zdarzenia (`"login"`, `"logout"`, `"purchase"`),
* czas zdarzenia (`time`) — liczba całkowita, rosnąca w skali całego systemu,
* kwotę (`amount`) — dla zdarzeń innych niż `"purchase"` zawsze `0`.

### Dane wejściowe

```python
events = [
    {"user_id": "u1", "type": "login",    "time": 1,  "amount": 0},
    {"user_id": "u1", "type": "purchase", "time": 5,  "amount": 120},
    {"user_id": "u1", "type": "logout",   "time": 10, "amount": 0},

    {"user_id": "u2", "type": "login",    "time": 12, "amount": 0},
    {"user_id": "u2", "type": "logout",   "time": 18, "amount": 0},

    {"user_id": "u3", "type": "login",    "time": 20, "amount": 0},
    {"user_id": "u3", "type": "purchase", "time": 25, "amount": 50},
    {"user_id": "u3", "type": "purchase", "time": 30, "amount": 75},
    {"user_id": "u3", "type": "logout",   "time": 40, "amount": 0},

    {"user_id": "u4", "type": "login",    "time": 45, "amount": 0},
    {"user_id": "u4", "type": "logout",   "time": 50, "amount": 0},
]
```

---

### Twoim zadaniem jest:

1. Zliczyć, ilu **unikalnych użytkowników** występuje w danych.
2. Obliczyć **łączną wartość zakupów** dla każdego użytkownika.
3. Obliczyć **łączny czas spędzony w systemie** przez każdego użytkownika
   (różnica `logout.time - login.time`).
4. Wypisać użytkowników, którzy:

   * wykonali co najmniej jeden `"login"`,
   * ale **nie wykonali żadnego `"purchase"`.
5. Wypisać użytkownika, który spędził **najwięcej czasu w systemie**.


"""