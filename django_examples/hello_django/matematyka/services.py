def add(a, b):
    return a + b

def sub(a, b):
    return a - b

def mul(a, b):
    return a * b

def div(a, b):
    return a / b


oprations = {
    "add": add,
    "sub": sub,
    "mul": mul,
    "div": div
}

class MathService:

    @staticmethod
    def calculate(op, a, b):
        return oprations[op](a, b)
