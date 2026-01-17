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


def decrypt(text, shift):
    result = ""
    for char in text:
        if char not in string.ascii_letters:
            result += char

        elif char.isupper():
            result += chr(
                (ord(char) - shift - 65) % 26 + 65
            )
        else:
            result += chr(
                (ord(char) - shift - 97) % 26 + 97
            )
    return result

