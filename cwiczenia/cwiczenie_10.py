"""
Utworz klase Cirlce, która pozwoli na tworzenie obiektow reprezentujacych kola

c = Circle(1)
assert c.rectangle == 3.14 * 2 * 1
assert c.area == 3.14 * 1 ** 2

"""
import pytest


class Circle:

    def __init__(self, radius):
        self.radius = radius

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        if value < 0:
            raise ValueError("Radius cannot be negative")
        self._radius = value

    @property
    def rectangle(self):
        return 3.14 * 2 * self.radius

    @rectangle.setter
    def rectangle(self, value):
        self.radius = value / (2 * 3.14)

    @property
    def area(self):
        return 3.14 * self.radius ** 2

    @area.setter
    def area(self, value):
        if value < 0:
            raise ValueError("Area cannot be negative")
        self.radius = (value / 3.14) ** 0.5


# pip install pytest
def test_valid_scenarios():
    c = Circle(1)

    assert c.rectangle == 3.14 * 2 * 1
    assert c.area == 3.14 * 1 ** 2

    c.radius = 2
    assert c.rectangle == 3.14 * 2 * 2
    assert c.area == 3.14 * 2 ** 2

    c.area = 3.14 * 16
    assert c.radius == 4

    c.rectangle = 3.14 * 2 * 17
    assert c.radius == 17


def test_invalid_scenarios():
    with pytest.raises(ValueError):
        Circle(-1)

    c = Circle(1)
    with pytest.raises(ValueError):
        c.radius = -10

    with pytest.raises(ValueError):
        c.area = -11

    with pytest.raises(ValueError):
        c.rectangle = -12
