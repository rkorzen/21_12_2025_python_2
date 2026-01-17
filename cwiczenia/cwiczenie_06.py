"""
### Zadanie

Napisz funkcję encrypt, która zaszyfruje tekst zgodnie z szyfrem cesara.
Oraz decrypt, która odkoduje ten tekst.

    >>> encrypt("CEASER CIPHER DEMO", 4)
    'GIEWIV GMTLIV HIQS'
    >>> decrypt("GIEWIV GMTLIV HIQS", 4)
    'CEASER CIPHER DEMO'

"""

import string

"ABCDEF...Z"
print(ord("A") - 65 + 4, ord("a") - 97)
print(ord("B") - 65, ord("b") - 97)
print(chr(ord("A") - 1))

def encrypt(text, shift):
    result = ""
    for char in text:
        if char not in string.ascii_letters:
            result += char

        elif char.isupper():
            result += chr(
                (ord(char) + shift - 65) % 26 + 65
            )
        else:
            result += chr(
                (ord(char) + shift - 97) % 26 + 97
            )
    return result

print(len("CEASER CIPHER DEMO"))

print(len(encrypt("CEASER CIPHER DEMO", 4)))
print(encrypt("CEASER CIPHER DEMO", 4))
print("GIEWIV GMTLIV HIQS" == encrypt("CEASER CIPHER DEMO", 4))


