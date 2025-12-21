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

    {"user_id": "u1", "type": "login",    "time": 55,  "amount": 0},
    {"user_id": "u1", "type": "purchase", "time": 60,  "amount": 120},
    {"user_id": "u1", "type": "logout",   "time": 70, "amount": 0},
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
from collections import defaultdict

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

    {"user_id": "u1", "type": "login",    "time": 55,  "amount": 0},
    {"user_id": "u1", "type": "purchase", "time": 60,  "amount": 120},
    {"user_id": "u1", "type": "logout",   "time": 70, "amount": 0},

    {"user_id": "u2", "type": "login", "time": 75, "amount": 0},
    {"user_id": "u2", "type": "purchase", "time": 80,  "amount": 200},
    {"user_id": "u2", "type": "logout", "time": 85, "amount": 0},

]

# 1. Unikalni uzytkownicy

users = {event["user_id"] for event in events}

print(f"Ilosc unikalnych uzytkownikow: {len(users)}")

# 2. łączna wartość zakupów

purchase_total = defaultdict(int)

for event in events:

    user = event["user_id"]

    if event["type"] == "purchase":
        purchase_total[user] += event["amount"]

print("Liczba zakupow dla poszczegolnych uzytkownikow:")
for user, total in sorted(purchase_total.items(), key=lambda x: x[1], reverse=True):
    print(f" - {user}: {total}")

# 3. czas spedzony w systemie

last_login = {}
time_spent = defaultdict(int)

for event in events:
    user = event["user_id"]
    e_type = event["type"]
    time = event["time"]

    if e_type == "login":
        last_login[user] = time
    elif e_type == "logout":
        session_time = time - last_login[user]
        time_spent[user] += session_time

print("Czas spedzony w systemie przez poszczegolnych uzytkownikow:")
for user, time in sorted(time_spent.items(), key=lambda x: x[1], reverse=True):
    print(f" - {user}: {time}")


# 4. login bez zakupu
logins = defaultdict(int)
purchased = defaultdict(int)

for event in events:
    user = event["user_id"]
    e_type = event["type"]

    if e_type == "login":
        logins[user] = event["time"]
    elif e_type == "purchase":
        purchased[user] = event["time"]

print("Uzytkownicy bez zakupow:")
for user in logins:
    if purchased[user] == 0:
        print(f"- {user}")


print("Uzytkownik z najwiekszym czasem w systemie:", sorted(purchase_total.items(), key=lambda x: x[1], reverse=True)[0][0])