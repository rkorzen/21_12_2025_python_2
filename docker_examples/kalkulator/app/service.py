def add(a, b):
    return a + b


def sub(a, b):
    return a - b


def mul(a, b):
    return a * b


def div(a, b):
    if b == 0:
        return "Nie mozna dzielic przez 0"
    return a / b


def pow(a, b):
    return a ** b


def modulo(a, b):
    return a % b


class CalculatorService:
    operations = {
        "+": add,
        "-": sub,
        "*": mul,
        "/": div,
        "**": pow,
        "%": modulo
    }

    @classmethod
    def calculate(cls, a, b, op):
        return cls.operations[op](a, b)
