def formatuj(*args, **kwargs):
    # print(args, kwargs)
    text = "\n".join(args)
    for key, value in kwargs.items():
        text = text.replace(f"${key}", str(value))
    return text
# print(dir(str)) # zobacz jak dziala join, replace przy pomocy help
# print(help(str.join))

assert formatuj("") == ""
assert formatuj("A", "B") == "A\nB"
assert formatuj("to jest tekst ze zmienna a=a", a=1) == "to jest tekst ze zmienna a=a"
assert formatuj("to jest tekst ze zmienna a=$a", a=1) == "to jest tekst ze zmienna a=1"
assert formatuj("to jest tekst ze zmienna a=$a", a="xyz") == "to jest tekst ze zmienna a=xyz"
assert formatuj("$x, $y", "$x, $z", "$z, $v", x=10, y=20, z="a", v="b", j="100") == "10, 20\n10, a\na, b"

