"""
Utworz klase Cirlce, która pozwoli na tworzenie obiektow reprezentujacych kola

c = Circle(1)
assert c.rectangle == 3.14 * 2 * 1
assert c.area == 3.14 * 1 ** 2

"""


c = Circle(1)
assert c.rectangle == 3.14 * 2 * 1
assert c.area == 3.14 * 1 ** 2

try:
    Circle(-1)
except ValueError as e:
    assert str(e) == "Radius cannot be negative"

