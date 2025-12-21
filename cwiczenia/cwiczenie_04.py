

print(dir(str)) # zobacz jak dziala join, replace przy pomocy help

assert format("") == ""
assert format("A", "B") == "A\nB"
assert format("to jest tekst ze zmienna a=$a", a=1) == "to jest tekst ze zmienna a=1"
assert format("to jest tekst ze zmienna a=$a", a="xyz") == "to jest tekst ze zmienna a=xyz"
assert format("$x, $y", "$x, $z", "$z, $v", x=10, y=20, z="a", v="b", j="100") == "10, 20\n10, a\na, b"

