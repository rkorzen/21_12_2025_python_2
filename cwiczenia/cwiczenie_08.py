"""

Napisz dekorator, ktory bedzie logowac uzycie funkcji, jej nazwe, argumenty, wynik i czas wykonania

"""

def logowanie(func):
    return func

@logowanie
def jakas_funkcja():
    ...

jakas_funkcja()

""" Powinno to printowac
Wywolano funkcje `jakas_funkcja` z parametrami: None, wynik: None, czas: 0.000000s
"""

import time
t1 = time.time()
time.sleep(1)
t2 = time.time()
print(f"Czas: {t2-t1}s")