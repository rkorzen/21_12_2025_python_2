"""
mamy liste, np

    dane = [1, 1, 2, 3, 1, 4, 5, 17, 21, 29]

napisz kod  (bez definiowania funkcji)

ktory z danej listy wybierze liczby pierwszze i zapisze je w nowe liscie


...

nowe_dane == [2, 3, 5, 17, 29]


"""

dane = [1, 1, 2, 3, 1, 4, 5, 17, 21, 29]
nowe_dane = []
for liczba in dane:
    if liczba < 2:
        continue

    for dzielnik in range(2, liczba):
        if liczba % dzielnik == 0:
            break
    else:
        nowe_dane.append(liczba)

print(nowe_dane)

assert nowe_dane == [2, 3, 5, 17, 29]
